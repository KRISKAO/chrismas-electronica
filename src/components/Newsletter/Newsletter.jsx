import React, { useState } from 'react';
import './Newsletter.module.css';

const Newsletter = () => {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`¡Gracias por suscribirte con ${email}! Recibirás nuestras ofertas.`);
    setEmail('');
  };

  return (
    <div className="newsletter">
      <div className="newsletter-content">
        <div className="newsletter-text">
          <h3>📧 ¡No te pierdas nuestras ofertas!</h3>
          <p>Suscríbete y recibe descuentos exclusivos, novedades y promociones especiales.</p>
        </div>
        <form onSubmit={handleSubmit} className="newsletter-form">
          <input
            type="email"
            placeholder="Tu correo electrónico"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <button type="submit">Suscribirme</button>
        </form>
      </div>
    </div>
  );
};

export default Newsletter;