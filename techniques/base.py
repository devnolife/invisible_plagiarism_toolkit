# techniques/base.py
"""
Base classes for steganography techniques
Plugin-style architecture for extensibility
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class TechniqueType(Enum):
    UNICODE_SUBSTITUTION = "unicode_substitution"
    INVISIBLE_CHARS = "invisible_chars"
    SPACING_MANIPULATION = "spacing_manipulation"
    METADATA_MANIPULATION = "metadata_manipulation"
    HEADER_MANIPULATION = "header_manipulation"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class TechniqueResult:
    """Result of applying a steganography technique"""
    success: bool
    changes_made: int
    risk_score: float
    detection_probability: float
    technique_name: str
    details: Dict[str, Any]
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []

class BaseTechnique(ABC):
    """Base class for all steganography techniques"""
    
    def __init__(self, config: Dict[str, Any], logger=None):
        self.config = config
        self.logger = logger
        self.enabled = config.get('enabled', True)
        self.risk_level = RiskLevel.MEDIUM
        
    @property
    @abstractmethod
    def technique_type(self) -> TechniqueType:
        """Return the type of this technique"""
        pass
    
    @property
    @abstractmethod
    def technique_name(self) -> str:
        """Return human-readable name of this technique"""
        pass
    
    @abstractmethod
    def apply(self, text: str, context: Dict[str, Any] = None) -> TechniqueResult:
        """Apply the technique to the given text"""
        pass
    
    @abstractmethod
    def calculate_risk_score(self, text: str, changes_made: int) -> float:
        """Calculate risk score for detection (0-1, higher = more risky)"""
        pass
    
    def is_applicable(self, text: str, context: Dict[str, Any] = None) -> bool:
        """Check if this technique is applicable to the given text"""
        return self.enabled and len(text.strip()) > 0
    
    def validate_config(self) -> bool:
        """Validate technique configuration"""
        return True
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get technique metadata for reporting"""
        return {
            'name': self.technique_name,
            'type': self.technique_type.value,
            'enabled': self.enabled,
            'risk_level': self.risk_level.value
        }

class TechniqueManager:
    """Manager for all steganography techniques"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.techniques: List[BaseTechnique] = []
        self.technique_registry: Dict[str, BaseTechnique] = {}
    
    def register_technique(self, technique: BaseTechnique):
        """Register a new technique"""
        self.techniques.append(technique)
        self.technique_registry[technique.technique_name] = technique
        
        if self.logger:
            self.logger.debug(f"Registered technique: {technique.technique_name}")
    
    def apply_techniques(
        self,
        text: str,
        context: Dict[str, Any] = None,
        technique_filter: List[str] = None
    ) -> List[TechniqueResult]:
        """Apply multiple techniques to text"""
        
        results = []
        current_text = text
        
        # Filter techniques if specified
        active_techniques = self.techniques
        if technique_filter:
            active_techniques = [
                t for t in self.techniques 
                if t.technique_name in technique_filter
            ]
        
        for technique in active_techniques:
            if not technique.is_applicable(current_text, context):
                continue
                
            try:
                result = technique.apply(current_text, context)
                results.append(result)
                
                # If successful, update text for next technique
                if result.success and 'modified_text' in result.details:
                    current_text = result.details['modified_text']
                    
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Technique {technique.technique_name} failed: {e}")
                
                # Create error result
                error_result = TechniqueResult(
                    success=False,
                    changes_made=0,
                    risk_score=0,
                    detection_probability=0,
                    technique_name=technique.technique_name,
                    details={'error': str(e)},
                    warnings=[f"Technique failed: {e}"]
                )
                results.append(error_result)
        
        return results
    
    def get_total_risk_score(self, results: List[TechniqueResult]) -> float:
        """Calculate combined risk score from multiple techniques"""
        if not results:
            return 0
        
        # Combine risk scores (weighted average based on changes made)
        total_changes = sum(r.changes_made for r in results if r.success)
        if total_changes == 0:
            return 0
        
        weighted_risk = sum(
            r.risk_score * r.changes_made 
            for r in results if r.success
        )
        
        return min(1.0, weighted_risk / total_changes)
    
    def list_techniques(self) -> List[Dict[str, Any]]:
        """List all registered techniques with metadata"""
        return [t.get_metadata() for t in self.techniques]
