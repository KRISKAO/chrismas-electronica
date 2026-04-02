import React from 'react';
import './HeroBanner.module.css';

const HeroBanner = () => {
  return (
    <div className="hero-banner">
      <div className="hero-content">
        <div className="hero-text">
          <h1 className="hero-title">
            El mayor stock de <span className="highlight">electrónica</span> en Bolivia
          </h1>
          <p className="hero-description">
            Encuentra todo para tus proyectos. Ofrecemos los mejores precios 
            en ventas por menor y descuentos exclusivos para compras por mayor a nivel nacional.
          </p>
          <div className="hero-buttons">
            <button className="btn-hero btn-hero-primary">
              Ver Catálogo Completo
            </button>
            <button className="btn-hero btn-hero-secondary">
              Ofertas Especiales
            </button>
          </div>
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-number">500+</span>
              <span className="stat-label">Productos</span>
            </div>
            <div className="stat">
              <span className="stat-number">9</span>
              <span className="stat-label">Departamentos</span>
            </div>
            <div className="stat">
              <span className="stat-number">24/7</span>
              <span className="stat-label">Soporte</span>
            </div>
          </div>
        </div>
        <div className="hero-image">
          <div className="hero-icon">🛒</div>
        </div>
      </div>
    </div>
  );
};

export default HeroBanner;