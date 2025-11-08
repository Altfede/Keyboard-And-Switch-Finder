"""Modello dati per Switch meccanici"""
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from enum import Enum


class SwitchFeel(str, Enum):
    LINEAR = "linear"
    TACTILE = "tactile"
    CLICKY = "clicky"


class HousingMaterial(str, Enum):
    POLYCARBONATE = "polycarbonate"
    NYLON = "nylon"
    POM = "pom"
    ABS = "abs"
    MIXED = "mixed"


class SoundProfile(str, Enum):
    THOCK = "thock"
    CLACK = "clack"
    MARBLY = "marbly"
    MUTED = "muted"
    CREAMY = "creamy"
    POPPY = "poppy"


class Switch(BaseModel):
    """Modello completo di uno switch meccanico"""

    # Identificazione
    id: str
    name: str
    brand: str

    # Caratteristiche meccaniche
    feel: SwitchFeel
    actuation_force: float = Field(ge=35, le=80, description="Forza attuazione in grammi")
    bottom_out_force: Optional[float] = Field(None, ge=40, le=90)
    actuation_travel: float = Field(default=2.0, ge=1.5, le=3.0, description="Distanza attuazione mm")
    total_travel: float = Field(default=4.0, ge=3.0, le=4.5, description="Corsa totale mm")

    # Caratteristiche costruttive
    top_housing: HousingMaterial
    bottom_housing: HousingMaterial
    stem_material: str = "POM"
    long_pole: bool = False
    pin_count: int = Field(ge=3, le=5)

    # Lubrificazione e smoothness
    factory_lubed: bool = False
    smoothness_rating: float = Field(ge=1, le=5, description="1=scratchy, 5=buttery smooth")

    # Suono
    sound_profile: List[SoundProfile] = []
    sound_level: float = Field(ge=1, le=5, description="1=silenzioso, 5=molto rumoroso")
    silent_variant: bool = False
    spring_ping: float = Field(ge=1, le=5, description="1=nessun ping, 5=molto ping")

    # Stabilità e wobble
    stem_wobble_xy: float = Field(ge=1, le=5, description="1=stabile, 5=molto wobble")

    # RGB e estetica
    transparent_housing: bool = False
    rgb_compatible: bool = True

    # Compatibilità
    mx_compatible: bool = True

    # Disponibilità e pricing
    availability_region: List[str] = ["EU"]
    stock_status: str = "in_stock"  # in_stock, backorder, group_buy, discontinued

    price_10: Optional[float] = None
    price_35: Optional[float] = None
    price_70: Optional[float] = None
    price_90: Optional[float] = None
    price_110: Optional[float] = None

    # Metadati
    verified: bool = False
    last_updated: str
    notes: Optional[str] = None
    audio_sample_url: Optional[str] = None

    # Vettore caratteristiche normalizzato (per scoring)
    def to_feature_vector(self) -> Dict[str, float]:
        """Converte lo switch in vettore di caratteristiche normalizzato"""
        return {
            # Feel (one-hot encoding)
            "feel_linear": 1.0 if self.feel == SwitchFeel.LINEAR else 0.0,
            "feel_tactile": 1.0 if self.feel == SwitchFeel.TACTILE else 0.0,
            "feel_clicky": 1.0 if self.feel == SwitchFeel.CLICKY else 0.0,

            # Peso normalizzato (35-80g -> 0-1)
            "actuation_force_norm": (self.actuation_force - 35) / 45,

            # Travel normalizzato (3.0-4.5mm -> 0-1)
            "travel_norm": (self.total_travel - 3.0) / 1.5,

            # Smoothness (già 1-5)
            "smoothness": self.smoothness_rating / 5.0,

            # Suono
            "sound_thock": 1.0 if SoundProfile.THOCK in self.sound_profile else 0.0,
            "sound_clack": 1.0 if SoundProfile.CLACK in self.sound_profile else 0.0,
            "sound_marbly": 1.0 if SoundProfile.MARBLY in self.sound_profile else 0.0,
            "sound_muted": 1.0 if SoundProfile.MUTED in self.sound_profile else 0.0,
            "sound_creamy": 1.0 if SoundProfile.CREAMY in self.sound_profile else 0.0,
            "sound_poppy": 1.0 if SoundProfile.POPPY in self.sound_profile else 0.0,

            # Caratteristiche binarie
            "silent": 1.0 if self.silent_variant else 0.0,
            "factory_lubed": 1.0 if self.factory_lubed else 0.0,
            "long_pole": 1.0 if self.long_pole else 0.0,
            "transparent_housing": 1.0 if self.transparent_housing else 0.0,

            # Wobble e ping invertiti (meno è meglio)
            "stability": 1.0 - (self.stem_wobble_xy / 5.0),
            "no_ping": 1.0 - (self.spring_ping / 5.0),

            # Pin count (normalizzato)
            "pin_5": 1.0 if self.pin_count == 5 else 0.0,

            # Housing material (one-hot per top housing)
            "housing_pc": 1.0 if self.top_housing == HousingMaterial.POLYCARBONATE else 0.0,
            "housing_nylon": 1.0 if self.top_housing == HousingMaterial.NYLON else 0.0,
            "housing_pom": 1.0 if self.top_housing == HousingMaterial.POM else 0.0,
        }

    def get_price_for_quantity(self, qty: int) -> Optional[float]:
        """Ottiene il prezzo per una quantità specifica"""
        if qty <= 10 and self.price_10:
            return self.price_10
        elif qty <= 35 and self.price_35:
            return self.price_35
        elif qty <= 70 and self.price_70:
            return self.price_70
        elif qty <= 90 and self.price_90:
            return self.price_90
        elif qty <= 110 and self.price_110:
            return self.price_110
        return None

    class Config:
        use_enum_values = True
