import React from 'react';
import './Navbar.module.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo">
          <h2>CHRISMAS</h2>
        </div>
        <div className="navbar-search">
          <input 
            type="text" 
            placeholder="Buscar componentes, módulos, herramientas..." 
          />
        </div>
        <div className="navbar-links">
          <a href="#">Mi Cuenta</a>
          <a href="#">Carrito</a>
        </div>
      </div>
      <div className="navbar-categories">
        <ul>
          <li><a href="#">Arduino & Módulos</a></li>
          <li><a href="#">Semiconductores</a></li>
          <li><a href="#">Pasivos</a></li>
          <li><a href="#">Herramientas</a></li>
          <li><a href="#">Ventas por Mayor</a></li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;