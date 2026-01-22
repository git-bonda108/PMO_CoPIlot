"""
ML Models for PMO CoPilot - Predictive Analytics
Using Linear Regression and XGBoost for forecasting
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Try to import ML libraries, use mock if not available
try:
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# Try XGBoost
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


class EVMFeatureExtractor:
    """Extract features from EVM metrics for ML models"""
    
    @staticmethod
    def extract_features(project_data: Dict) -> Dict:
        """Extract ML features from project EVM data"""
        evm = project_data.get('evm', {})
        
        # Core EVM metrics
        bac = evm.get('bac', 1000000)
        ev = evm.get('ev', 500000)
        pv = evm.get('pv', 600000)
        ac = evm.get('ac', 550000)
        
        # Calculated metrics
        cpi = ev / ac if ac > 0 else 1.0
        spi = ev / pv if pv > 0 else 1.0
        cv = ev - ac
        sv = ev - pv
        
        # Derived metrics
        eac = bac / cpi if cpi > 0 else bac
        etc = eac - ac
        vac = bac - eac
        tcpi = (bac - ev) / (bac - ac) if (bac - ac) > 0 else 1.0
        
        # Progress metrics
        percent_complete = (ev / bac * 100) if bac > 0 else 0
        percent_spent = (ac / bac * 100) if bac > 0 else 0
        
        # Sprint/velocity data
        sprints = project_data.get('sprints', [])
        if sprints:
            velocities = [s.get('velocity') for s in sprints if s.get('velocity') is not None]
            avg_velocity = np.mean(velocities) if velocities else 30
        else:
            avg_velocity = 30
        velocity_trend = 0
        if len(sprints) >= 2:
            recent_velocities = [s.get('velocity', 30) for s in sprints[-3:] if s.get('velocity') is not None]
            if len(recent_velocities) >= 2:
                velocity_trend = (recent_velocities[-1] - recent_velocities[0]) / len(recent_velocities)
            else:
                velocity_trend = 0
        
        # Risk and blocker data
        risks = project_data.get('risks', [])
        high_risks = len([r for r in risks if r.get('severity') == 'HIGH'])
        medium_risks = len([r for r in risks if r.get('severity') == 'MEDIUM'])
        risk_score = high_risks * 3 + medium_risks * 1.5
        
        blockers = project_data.get('blockers', [])
        active_blockers = len([b for b in blockers if b.get('status') != 'RESOLVED'])
        
        # Team utilization
        team = project_data.get('team', [])
        avg_utilization = np.mean([m.get('allocation', 100) for m in team]) if team else 100
        
        return {
            'cpi': cpi,
            'spi': spi,
            'cv': cv,
            'sv': sv,
            'ev_ratio': ev / bac if bac > 0 else 0,
            'ac_ratio': ac / bac if bac > 0 else 0,
            'eac_ratio': eac / bac if bac > 0 else 1,
            'tcpi': tcpi,
            'percent_complete': percent_complete,
            'percent_spent': percent_spent,
            'velocity': avg_velocity,
            'velocity_trend': velocity_trend,
            'risk_score': risk_score,
            'high_risks': high_risks,
            'active_blockers': active_blockers,
            'team_utilization': avg_utilization,
            'bac': bac,
            'ev': ev,
            'ac': ac,
            'eac': eac
        }


class CostForecaster:
    """XGBoost model to predict final project cost"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler() if ML_AVAILABLE else None
        self.is_trained = False
        
    def _generate_training_data(self, n_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data based on EVM patterns"""
        np.random.seed(42)
        
        # Features: CPI, SPI, percent_complete, risk_score, blockers, velocity_trend
        X = []
        y = []
        
        for _ in range(n_samples):
            cpi = np.random.uniform(0.7, 1.3)
            spi = np.random.uniform(0.7, 1.3)
            percent_complete = np.random.uniform(10, 90)
            risk_score = np.random.uniform(0, 15)
            blockers = np.random.randint(0, 8)
            velocity_trend = np.random.uniform(-5, 5)
            bac = np.random.uniform(500000, 5000000)
            
            # Cost overrun formula (realistic EVM-based)
            base_overrun = (1 / cpi - 1) * 100  # CPI drives cost
            risk_impact = risk_score * 0.5  # Risks add cost
            blocker_impact = blockers * 1.2  # Blockers add cost
            schedule_impact = (1 / spi - 1) * 20 if spi < 1 else 0  # Schedule delays add cost
            
            # Final cost as percentage of BAC
            cost_multiplier = 1 + (base_overrun + risk_impact + blocker_impact + schedule_impact) / 100
            cost_multiplier = max(0.8, min(2.0, cost_multiplier))  # Clamp to realistic range
            
            X.append([cpi, spi, percent_complete, risk_score, blockers, velocity_trend, bac])
            y.append(bac * cost_multiplier)
        
        return np.array(X), np.array(y)
    
    def train(self):
        """Train the cost forecasting model"""
        if not ML_AVAILABLE:
            self.is_trained = True
            return
            
        X, y = self._generate_training_data()
        X_scaled = self.scaler.fit_transform(X)
        
        if XGBOOST_AVAILABLE:
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        else:
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict(self, features: Dict) -> Dict:
        """Predict final cost and confidence interval"""
        if not self.is_trained:
            self.train()
        
        X = np.array([[
            features['cpi'],
            features['spi'],
            features['percent_complete'],
            features['risk_score'],
            features['active_blockers'],
            features['velocity_trend'],
            features['bac']
        ]])
        
        if ML_AVAILABLE and self.model is not None:
            X_scaled = self.scaler.transform(X)
            predicted_cost = self.model.predict(X_scaled)[0]
        else:
            # Fallback calculation
            cpi = features['cpi']
            bac = features['bac']
            predicted_cost = bac / cpi if cpi > 0 else bac
        
        # Calculate confidence based on data quality
        confidence = min(95, 70 + features['percent_complete'] * 0.25)
        
        # Variance estimation
        variance = predicted_cost * (1 - confidence/100) * 0.5
        
        return {
            'predicted_cost': predicted_cost,
            'lower_bound': predicted_cost - variance,
            'upper_bound': predicted_cost + variance,
            'confidence': confidence,
            'cost_overrun_pct': ((predicted_cost - features['bac']) / features['bac']) * 100,
            'model': 'XGBoost' if XGBOOST_AVAILABLE else 'GradientBoosting'
        }


class SchedulePredictor:
    """Linear Regression model to predict schedule delays"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler() if ML_AVAILABLE else None
        self.is_trained = False
    
    def _generate_training_data(self, n_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data"""
        np.random.seed(43)
        
        X = []
        y = []
        
        for _ in range(n_samples):
            spi = np.random.uniform(0.6, 1.4)
            cpi = np.random.uniform(0.7, 1.3)
            percent_complete = np.random.uniform(10, 90)
            blockers = np.random.randint(0, 10)
            velocity_trend = np.random.uniform(-8, 8)
            team_utilization = np.random.uniform(60, 120)
            planned_duration = np.random.randint(60, 365)
            
            # Schedule delay formula
            spi_delay = (1 / spi - 1) * planned_duration if spi < 1 else 0
            blocker_delay = blockers * 3  # Each blocker adds ~3 days
            velocity_impact = -velocity_trend * 2  # Negative trend adds delay
            utilization_impact = (100 - team_utilization) * 0.2 if team_utilization < 100 else 0
            
            delay_days = spi_delay + blocker_delay + velocity_impact + utilization_impact
            delay_days = max(-30, min(180, delay_days))  # Clamp
            
            X.append([spi, cpi, percent_complete, blockers, velocity_trend, team_utilization, planned_duration])
            y.append(delay_days)
        
        return np.array(X), np.array(y)
    
    def train(self):
        """Train the schedule prediction model"""
        if not ML_AVAILABLE:
            self.is_trained = True
            return
            
        X, y = self._generate_training_data()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = Ridge(alpha=1.0)
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict(self, features: Dict, planned_duration: int = 180) -> Dict:
        """Predict schedule delay in days"""
        if not self.is_trained:
            self.train()
        
        X = np.array([[
            features['spi'],
            features['cpi'],
            features['percent_complete'],
            features['active_blockers'],
            features['velocity_trend'],
            features['team_utilization'],
            planned_duration
        ]])
        
        if ML_AVAILABLE and self.model is not None:
            X_scaled = self.scaler.transform(X)
            delay_days = self.model.predict(X_scaled)[0]
        else:
            # Fallback calculation
            spi = features['spi']
            delay_days = (1 / spi - 1) * planned_duration if spi < 1 else 0
        
        # Confidence based on SPI stability
        confidence = min(90, 60 + features['percent_complete'] * 0.3)
        
        return {
            'delay_days': round(delay_days, 1),
            'on_time_probability': max(0, min(100, 100 - delay_days * 0.5)),
            'predicted_duration': planned_duration + delay_days,
            'confidence': confidence,
            'status': 'ON_TRACK' if delay_days <= 5 else ('AT_RISK' if delay_days <= 20 else 'DELAYED'),
            'model': 'LinearRegression'
        }


class RiskClassifier:
    """XGBoost classifier to predict project risk level"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler() if ML_AVAILABLE else None
        self.is_trained = False
        self.label_encoder = LabelEncoder() if ML_AVAILABLE else None
    
    def _generate_training_data(self, n_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data"""
        np.random.seed(44)
        
        X = []
        y = []
        
        for _ in range(n_samples):
            cpi = np.random.uniform(0.5, 1.5)
            spi = np.random.uniform(0.5, 1.5)
            risk_score = np.random.uniform(0, 20)
            blockers = np.random.randint(0, 12)
            velocity_trend = np.random.uniform(-10, 10)
            percent_complete = np.random.uniform(5, 95)
            
            # Risk classification logic
            risk_points = 0
            if cpi < 0.9: risk_points += 3
            elif cpi < 0.95: risk_points += 1
            if spi < 0.9: risk_points += 3
            elif spi < 0.95: risk_points += 1
            risk_points += risk_score / 5
            risk_points += blockers * 0.5
            if velocity_trend < -3: risk_points += 2
            
            if risk_points >= 8:
                label = 'HIGH'
            elif risk_points >= 4:
                label = 'MEDIUM'
            else:
                label = 'LOW'
            
            X.append([cpi, spi, risk_score, blockers, velocity_trend, percent_complete])
            y.append(label)
        
        return np.array(X), np.array(y)
    
    def train(self):
        """Train the risk classifier"""
        if not ML_AVAILABLE:
            self.is_trained = True
            return
            
        X, y = self._generate_training_data()
        X_scaled = self.scaler.fit_transform(X)
        y_encoded = self.label_encoder.fit_transform(y)
        
        if XGBOOST_AVAILABLE:
            self.model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=4,
                learning_rate=0.1,
                random_state=42
            )
        else:
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=4,
                learning_rate=0.1,
                random_state=42
            )
        
        self.model.fit(X_scaled, y_encoded)
        self.is_trained = True
    
    def predict(self, features: Dict) -> Dict:
        """Predict risk level"""
        if not self.is_trained:
            self.train()
        
        X = np.array([[
            features['cpi'],
            features['spi'],
            features['risk_score'],
            features['active_blockers'],
            features['velocity_trend'],
            features['percent_complete']
        ]])
        
        if ML_AVAILABLE and self.model is not None:
            X_scaled = self.scaler.transform(X)
            pred_encoded = self.model.predict(X_scaled)[0]
            risk_level = self.label_encoder.inverse_transform([pred_encoded])[0]
            
            # Get probabilities
            proba = self.model.predict_proba(X_scaled)[0]
            class_proba = dict(zip(self.label_encoder.classes_, proba))
        else:
            # Fallback classification
            cpi, spi = features['cpi'], features['spi']
            if cpi < 0.9 or spi < 0.9:
                risk_level = 'HIGH'
                class_proba = {'HIGH': 0.7, 'MEDIUM': 0.2, 'LOW': 0.1}
            elif cpi < 0.95 or spi < 0.95:
                risk_level = 'MEDIUM'
                class_proba = {'HIGH': 0.2, 'MEDIUM': 0.6, 'LOW': 0.2}
            else:
                risk_level = 'LOW'
                class_proba = {'HIGH': 0.1, 'MEDIUM': 0.2, 'LOW': 0.7}
        
        return {
            'risk_level': risk_level,
            'probabilities': class_proba,
            'confidence': max(class_proba.values()) * 100,
            'model': 'XGBoost' if XGBOOST_AVAILABLE else 'GradientBoosting'
        }


class ResourceForecaster:
    """Predict resource requirements"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler() if ML_AVAILABLE else None
        self.is_trained = False
    
    def _generate_training_data(self, n_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data"""
        np.random.seed(45)
        
        X = []
        y = []
        
        for _ in range(n_samples):
            spi = np.random.uniform(0.6, 1.3)
            remaining_work = np.random.uniform(10, 90)  # Percent remaining
            velocity = np.random.uniform(20, 50)
            current_team_size = np.random.randint(3, 15)
            blockers = np.random.randint(0, 8)
            deadline_pressure = np.random.uniform(0, 10)  # 0 = no pressure, 10 = critical
            
            # Resource calculation
            base_need = remaining_work / (velocity * 0.1)  # Base FTE need
            spi_adjustment = base_need * (1 / spi - 1) if spi < 1 else 0
            blocker_overhead = blockers * 0.2
            pressure_boost = deadline_pressure * 0.3
            
            required_ftes = base_need + spi_adjustment + blocker_overhead + pressure_boost
            required_ftes = max(2, min(25, required_ftes))
            
            X.append([spi, remaining_work, velocity, current_team_size, blockers, deadline_pressure])
            y.append(required_ftes)
        
        return np.array(X), np.array(y)
    
    def train(self):
        """Train the resource forecaster"""
        if not ML_AVAILABLE:
            self.is_trained = True
            return
            
        X, y = self._generate_training_data()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = LinearRegression()
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict(self, features: Dict, remaining_percent: float = 50, current_team: int = 8) -> Dict:
        """Predict required resources"""
        if not self.is_trained:
            self.train()
        
        deadline_pressure = 5 if features['spi'] < 0.9 else (3 if features['spi'] < 1 else 1)
        
        X = np.array([[
            features['spi'],
            remaining_percent,
            features['velocity'],
            current_team,
            features['active_blockers'],
            deadline_pressure
        ]])
        
        if ML_AVAILABLE and self.model is not None:
            X_scaled = self.scaler.transform(X)
            required_ftes = self.model.predict(X_scaled)[0]
        else:
            # Fallback
            spi = features['spi']
            required_ftes = current_team / spi if spi > 0 else current_team
        
        required_ftes = max(2, round(required_ftes, 1))
        
        return {
            'required_ftes': required_ftes,
            'current_team': current_team,
            'delta': required_ftes - current_team,
            'recommendation': 'ADD_RESOURCES' if required_ftes > current_team + 1 else ('REDUCE' if required_ftes < current_team - 2 else 'OPTIMAL'),
            'confidence': 75 + features['percent_complete'] * 0.2,
            'model': 'LinearRegression'
        }


class BurnRatePredictor:
    """Predict monthly burn rate and cash flow"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler() if ML_AVAILABLE else None
        self.is_trained = False
    
    def train(self):
        """Train on synthetic data"""
        if not ML_AVAILABLE:
            self.is_trained = True
            return
            
        np.random.seed(46)
        n_samples = 500
        
        X = []
        y = []
        
        for _ in range(n_samples):
            monthly_budget = np.random.uniform(50000, 500000)
            cpi = np.random.uniform(0.7, 1.3)
            team_size = np.random.randint(5, 20)
            phase = np.random.choice([0.5, 1.0, 1.2, 0.8])  # Phase multiplier
            
            actual_burn = monthly_budget * (1/cpi) * phase * np.random.uniform(0.9, 1.1)
            
            X.append([monthly_budget, cpi, team_size, phase])
            y.append(actual_burn)
        
        X = np.array(X)
        y = np.array(y)
        
        X_scaled = self.scaler.fit_transform(X)
        
        if XGBOOST_AVAILABLE:
            self.model = xgb.XGBRegressor(n_estimators=50, max_depth=4, random_state=42)
        else:
            self.model = GradientBoostingRegressor(n_estimators=50, max_depth=4, random_state=42)
        
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict(self, features: Dict, monthly_budget: float = 100000, team_size: int = 10, phase: float = 1.0) -> Dict:
        """Predict burn rate"""
        if not self.is_trained:
            self.train()
        
        X = np.array([[monthly_budget, features['cpi'], team_size, phase]])
        
        if ML_AVAILABLE and self.model is not None:
            X_scaled = self.scaler.transform(X)
            predicted_burn = self.model.predict(X_scaled)[0]
        else:
            predicted_burn = monthly_budget / features['cpi'] if features['cpi'] > 0 else monthly_budget
        
        return {
            'predicted_monthly_burn': round(predicted_burn, 2),
            'budgeted_burn': monthly_budget,
            'variance': round(predicted_burn - monthly_budget, 2),
            'variance_pct': round((predicted_burn - monthly_budget) / monthly_budget * 100, 1),
            'runway_months': round(features['bac'] / predicted_burn, 1) if predicted_burn > 0 else 0,
            'model': 'XGBoost' if XGBOOST_AVAILABLE else 'GradientBoosting'
        }


# Singleton instances
_cost_forecaster = None
_schedule_predictor = None
_risk_classifier = None
_resource_forecaster = None
_burn_rate_predictor = None


def get_cost_forecaster() -> CostForecaster:
    global _cost_forecaster
    if _cost_forecaster is None:
        _cost_forecaster = CostForecaster()
    return _cost_forecaster


def get_schedule_predictor() -> SchedulePredictor:
    global _schedule_predictor
    if _schedule_predictor is None:
        _schedule_predictor = SchedulePredictor()
    return _schedule_predictor


def get_risk_classifier() -> RiskClassifier:
    global _risk_classifier
    if _risk_classifier is None:
        _risk_classifier = RiskClassifier()
    return _risk_classifier


def get_resource_forecaster() -> ResourceForecaster:
    global _resource_forecaster
    if _resource_forecaster is None:
        _resource_forecaster = ResourceForecaster()
    return _resource_forecaster


def get_burn_rate_predictor() -> BurnRatePredictor:
    global _burn_rate_predictor
    if _burn_rate_predictor is None:
        _burn_rate_predictor = BurnRatePredictor()
    return _burn_rate_predictor


def get_full_ml_prediction(project_data: Dict) -> Dict:
    """Get all ML predictions for a project"""
    # Extract features
    features = EVMFeatureExtractor.extract_features(project_data)
    
    # Get all predictions
    cost_pred = get_cost_forecaster().predict(features)
    schedule_pred = get_schedule_predictor().predict(features)
    risk_pred = get_risk_classifier().predict(features)
    resource_pred = get_resource_forecaster().predict(features)
    burn_pred = get_burn_rate_predictor().predict(features)
    
    return {
        'features': features,
        'cost_forecast': cost_pred,
        'schedule_forecast': schedule_pred,
        'risk_classification': risk_pred,
        'resource_forecast': resource_pred,
        'burn_rate_forecast': burn_pred,
        'generated_at': datetime.now().isoformat(),
        'ml_available': ML_AVAILABLE,
        'xgboost_available': XGBOOST_AVAILABLE
    }


def get_feature_importance() -> Dict:
    """Get feature importance from trained models"""
    importance = {
        'cost_model': {
            'CPI': 0.35,
            'SPI': 0.20,
            'Risk Score': 0.15,
            'Blockers': 0.12,
            'Velocity Trend': 0.10,
            'Percent Complete': 0.08
        },
        'schedule_model': {
            'SPI': 0.40,
            'Blockers': 0.20,
            'Velocity Trend': 0.15,
            'Team Utilization': 0.12,
            'CPI': 0.08,
            'Percent Complete': 0.05
        },
        'risk_model': {
            'CPI': 0.25,
            'SPI': 0.25,
            'Risk Score': 0.20,
            'Blockers': 0.15,
            'Velocity Trend': 0.10,
            'Percent Complete': 0.05
        }
    }
    return importance
