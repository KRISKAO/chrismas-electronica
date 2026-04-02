import React, { useState } from 'react';
import './ProductCard.module.css';

const ProductCard = ({ product }) => {
  const [isHovered, setIsHovered] = useState(false);

  const formatPrice = (price) => {
    return `Bs. ${price.toFixed(2)}`;
  };

  const hasWholesale = product.wholesalePrice && product.wholesaleQuantity;

  return (
    <div 
      className={`product-card ${isHovered ? 'hovered' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="product-badge">
        {product.inStock ? (
          <span className="badge in-stock">En Stock</span>
        ) : (
          <span className="badge out-stock">Agotado</span>
        )}
        {hasWholesale && (
          <span className="badge wholesale">Oferta Mayor</span>
        )}
      </div>
      
      <div className="product-image">
        <div className="image-placeholder">
          {product.category === 'Placas de Desarrollo' && '🔌'}
          {product.category === 'Sensores' && '📡'}
          {product.category === 'Pasivos' && '🔧'}
          {product.category === 'Semiconductores' && '⚡'}
          {!product.category && '📦'}
        </div>
      </div>
      
      <div className="product-info">
        <div className="product-category">{product.category}</div>
        <h3 className="product-title">{product.name}</h3>
        <p className="product-reference">{product.reference}</p>
        
        <div className="product-pricing">
          <div className="price-unit">
            <span className="price-label">Precio unitario:</span>
            <span className="price-value">{formatPrice(product.price)}</span>
          </div>
          
          {hasWholesale && (
            <div className="price-wholesale">
              <span className="price-label">
                Por Mayor (&gt;{product.wholesaleQuantity}u):
              </span>
              <span className="price-value wholesale-price">
                {formatPrice(product.wholesalePrice)}
              </span>
            </div>
          )}
        </div>
        
        <button 
          className="btn-add-to-cart"
          disabled={!product.inStock}
        >
          {product.inStock ? 'Agregar al Carrito' : 'No Disponible'}
        </button>
      </div>
    </div>
  );
};

export default ProductCard;