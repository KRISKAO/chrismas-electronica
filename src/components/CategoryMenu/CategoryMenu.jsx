import React, { useState } from 'react';
import './CategoryMenu.module.css';

const CategoryMenu = () => {
  const [activeCategory, setActiveCategory] = useState('todos');

  const categories = [
    { id: 'todos', name: 'Todos los productos', icon: '📦' },
    { id: 'arduino', name: 'Arduino & Módulos', icon: '🔌' },
    { id: 'semiconductores', name: 'Semiconductores', icon: '⚡' },
    { id: 'pasivos', name: 'Pasivos', icon: '🔧' },
    { id: 'herramientas', name: 'Herramientas', icon: '🛠️' },
    { id: 'sensores', name: 'Sensores', icon: '📡' },
    { id: 'prototipado', name: 'Prototipado', icon: '🔬' },
    { id: 'mayor', name: 'Ventas por Mayor', icon: '🏪' }
  ];

  return (
    <div className="category-menu">
      <div className="category-container">
        <div className="category-header">
          <h3>Categorías</h3>
        </div>
        <ul className="category-list">
          {categories.map(category => (
            <li key={category.id}>
              <button
                className={`category-btn ${activeCategory === category.id ? 'active' : ''}`}
                onClick={() => setActiveCategory(category.id)}
              >
                <span className="category-icon">{category.icon}</span>
                <span className="category-name">{category.name}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default CategoryMenu;