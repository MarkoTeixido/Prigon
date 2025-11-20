# tests/conftest.py
"""
Fixtures compartidos para todos los tests
"""

import pytest
from datetime import datetime
from src.models.evento import Evento


@pytest.fixture
def evento_ejemplo():
    """Fixture con un evento de ejemplo"""
    return Evento(
        fecha=datetime(2025, 12, 15, 9, 0),
        titulo="Examen de Matemáticas",
        categoria="examen"
    )


@pytest.fixture
def lista_eventos():
    """Fixture con lista de eventos variados"""
    return [
        Evento(
            fecha=datetime(2025, 12, 15, 9, 0),
            titulo="Examen de Matemáticas",
            categoria="examen"
        ),
        Evento(
            fecha=datetime(2025, 12, 20, 0, 0),
            titulo="Receso de Verano",
            categoria="receso"
        ),
        Evento(
            fecha=datetime(2025, 11, 21, 0, 0),
            titulo="Día no laborable",
            categoria="feriado"
        ),
    ]


@pytest.fixture
def html_calendario_mock():
    """HTML de ejemplo del calendario UNViMe"""
    return """
    <div class="cal-grid">
        <div class="cal-month">
            <h3>Diciembre</h3>
            <div class="cal-event-list">
                <div class="cal-event-item categoria-examen">
                    <span class="cal-event-date">15</span>
                    <span class="cal-event-title">. Examen de Matemáticas</span>
                </div>
                <div class="cal-event-item categoria-receso">
                    <span class="cal-event-date">20/12 al 31/12</span>
                    <span class="cal-event-title">. Receso de Verano</span>
                </div>
            </div>
        </div>
    </div>
    """


@pytest.fixture
def mock_cache(tmp_path):
    """Cache temporal para tests"""
    from src.utils.cache import Cache
    cache = Cache(cache_dir=str(tmp_path / "cache"), ttl_hours=1)
    return cache