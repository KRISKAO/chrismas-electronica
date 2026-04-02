import React from 'react';
import HeroBanner from '../../components/HeroBanner/HeroBanner';
import CategoryMenu from '../../components/CategoryMenu/CategoryMenu';
import ProductCard from '../../components/ProductCard/ProductCard';
import Newsletter from '../../components/Newsletter/Newsletter';
import { products } from '../../data/products';
import './HomePage.module.css';

const HomePage = () => {
  // Productos destacados (primeros 6)
  const featuredProducts = products.slice(0, 6);

  return (
    <div className="homepage">
      <HeroBanner />
      
      <div className="section">
        <div className="section-header">
          <h2>⚡ Productos Destacados</h2>
          <a href="/catalogo" className="view-all">Ver todos →</a>
        </div>
        <div className="products-grid">
          {featuredProducts.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>

      <CategoryMenu />

      <div className="section">
        <div className="section-header">
          <h2>📦 Últimos Productos</h2>
          <a href="/catalogo" className="view-all">Ver todos →</a>
        </div>
        <div className="products-grid">
          {products.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>

      <Newsletter />

      {/* Sección de ventajas */}
      <div className="features-section">
        <div className="features-grid">
          <div className="feature">
            <div className="feature-icon">🚚</div>
            <h3>Envíos Nacionales</h3>
            <p>Despachos diarios a los 9 departamentos de Bolivia</p>
          </div>
          <div className="feature">
            <div className="feature-icon">💰</div>
            <h3>Precios Mayoristas</h3>
            <p>Descuentos por volumen para talleres y empresas</p>
          </div>
          <div className="feature">
            <div className="feature-icon">✅</div>
            <h3>Garantía CHRISMAS</h3>
            <p>Componentes probados y garantizados</p>
          </div>
          <div className="feature">
            <div className="feature-icon">🔧</div>
            <h3>Soporte Técnico</h3>
            <p>Asesoramiento para tus proyectos</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;