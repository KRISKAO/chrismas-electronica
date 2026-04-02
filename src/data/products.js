// Datos de productos simulados para CHRISMAS Electrónica

export const products = [
  {
    id: 1,
    name: "Arduino Uno R3 Compatible + Cable USB",
    price: 55.00,
    wholesalePrice: 42.00,
    wholesaleQuantity: 10,
    category: "Placas de Desarrollo",
    reference: "CHR-MCU-001",
    description: "Placa de desarrollo compatible con Arduino Uno R3, incluye cable USB",
    inStock: true
  },
  {
    id: 2,
    name: "Pack Resistencias 10k Ohm 1/4W (100 pzas)",
    price: 12.00,
    wholesalePrice: 8.00,
    wholesaleQuantity: 10,
    category: "Pasivos",
    reference: "CHR-PAS-001",
    description: "Pack de 100 resistencias de 10k ohm, 1/4W, tolerancia 5%",
    inStock: true
  },
  {
    id: 3,
    name: "Módulo Relay 1 Canal 5V Optoacoplado",
    price: 15.00,
    wholesalePrice: 11.00,
    wholesaleQuantity: 12,
    category: "Módulos",
    reference: "CHR-MOD-001",
    description: "Módulo relé de 1 canal con optoacoplador, activo en bajo nivel",
    inStock: true
  },
  {
    id: 4,
    name: "Transistor NPN 2N2222A TO-92",
    price: 1.50,
    wholesalePrice: 0.80,
    wholesaleQuantity: 50,
    category: "Semiconductores",
    reference: "CHR-SEM-001",
    description: "Transistor NPN 2N2222A en encapsulado TO-92, ideal para conmutación",
    inStock: true
  },
  {
    id: 5,
    name: "Sensor Ultrasónico de Distancia HC-SR04",
    price: 15.00,
    wholesalePrice: 10.00,
    wholesaleQuantity: 20,
    category: "Sensores",
    reference: "CHR-SEN-045",
    description: "Sensor ultrasónico para medición de distancia de 2cm a 400cm",
    inStock: true
  }
];

export default products;
