import React from 'react';
import './Footer.module.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>CHRISMAS</h3>
          <p>Tu tienda de componentes electrónicos en Bolivia.</p>
          <p>Calidad, garantía y los mejores precios.</p>
        </div>
        <div className="footer-section">
          <h3>Contáctanos</h3>
          <p>Av. 6 de Agosto #1234, La Paz, Bolivia</p>
          <p>+591 71234567</p>
          <p>ventas@chrismaselectronica.com.bo</p>
        </div>
        <div className="footer-section">
          <h3>Envíos</h3>
          <p>Envíos a Santa Cruz</p>
          <p>Envíos a Cochabamba</p>
          <p>Envíos al interior del País</p>
        </div>
        <div className="footer-section">
          <h3>Métodos de Pago</h3>
          <p>Transferencia Bancaria</p>
          <p>Código QR Simple</p>
          <p>Tigo Money</p>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; 2024 CHRISMAS Electrónica. Todos los derechos reservados.</p>
      </div>
    </footer>
  );
};

export default Footer;  