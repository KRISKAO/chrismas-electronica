import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. INGRESO Y VALIDACIÓN DE DATOS
# ==========================================
while True:
    entrada = input("Ingresa una secuencia de bits (máximo 14 bits): ").strip()
    if not entrada or len(entrada) > 14 or not all(bit in ['0', '1'] for bit in entrada):
        print("❌ Error: Ingresa una secuencia válida de hasta 14 bits (solo 0s y 1s).")
        continue
    bits = np.array([int(bit) for bit in entrada])
    break

# ==========================================
# 2. CONFIGURACIÓN DE PARÁMETROS
# ==========================================
amplitud = 5            
muestras_por_bit = 100  
mitad = muestras_por_bit // 2

senales = {
    'NRZ-L': [], 'NRZ-I': [], 'Manchester': [], 
    'Manchester Dif.': [], 'AMI': [], 'MLT-3': []
}

# --- ESTADOS INICIALES ---
# Ajustado según tu imagen: comenzamos en -V para que el primer '1' suba a +V
estado_nrzi = -amplitud          
ultimo_nrz_dif = amplitud       
ultimo_voltaje_ami = -amplitud  
niveles_mlt3 = [0, amplitud, 0, -amplitud]
indice_mlt3 = 0                 

# ==========================================
# 3. GENERACIÓN DE LOS CÓDIGOS DE LÍNEA
# ==========================================
for bit in bits:
    # --- NRZ-L ---
    senales['NRZ-L'].extend([amplitud if bit == 1 else -amplitud] * muestras_por_bit)
    
    # --- NRZ-I (Basado en tu imagen) ---
    if bit == 1:
        estado_nrzi = -estado_nrzi  # Traslación (inversión) si es 1
    senales['NRZ-I'].extend([estado_nrzi] * muestras_por_bit)
    
    # --- Manchester (IEEE 802.3) ---
    if bit == 0:
        senales['Manchester'].extend([amplitud]*mitad + [-amplitud]*mitad)
    else:
        senales['Manchester'].extend([-amplitud]*mitad + [amplitud]*mitad)
    
    # --- Manchester Diferencial ---
    nivel_inicial = -ultimo_nrz_dif if bit == 0 else ultimo_nrz_dif
    senales['Manchester Dif.'].extend([nivel_inicial]*mitad + [-nivel_inicial]*mitad)
    ultimo_nrz_dif = -nivel_inicial
    
    # --- AMI ---
    if bit == 0:
        voltaje_ami = 0
    else:
        voltaje_ami = -ultimo_voltaje_ami  
        ultimo_voltaje_ami = voltaje_ami
    senales['AMI'].extend([voltaje_ami] * muestras_por_bit)
    
    # --- MLT-3 ---
    if bit == 1:
        indice_mlt3 = (indice_mlt3 + 1) % 4  
    senales['MLT-3'].extend([niveles_mlt3[indice_mlt3]] * muestras_por_bit)

tiempo = np.linspace(0, len(bits), len(senales['NRZ-L']))

# ==========================================
# 4. DESPLIEGUE VISUAL
# ==========================================
lista_codigos = ['NRZ-L', 'NRZ-I', 'Manchester', 'Manchester Dif.', 'AMI', 'MLT-3']
colores = ['blue', 'darkcyan', 'red', 'crimson', 'green', 'purple']

plt.figure(figsize=(12, 14))
tamano_fuente = 11 if len(bits) <= 8 else 9

for idx, nombre in enumerate(lista_codigos):
    ax = plt.subplot(6, 1, idx + 1)
    plt.plot(tiempo, senales[nombre], color=colores[idx], linewidth=2.5)
    
    plt.title(f'Código de Línea: {nombre}', fontsize=11, fontweight='bold', loc='left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.ylim(-amplitud - 2, amplitud + 2)
    plt.yticks([-amplitud, 0, amplitud], ['-V', '0', '+V'])
    plt.axhline(0, color='black', linewidth=0.8, alpha=0.3) # Línea base más clara
    
    # Líneas verticales de división de bits
    for i in range(len(bits) + 1):
        plt.axvline(i, color='gray', linestyle=':', alpha=0.5)
    
    # Etiquetas de bits
    for i, bit in enumerate(bits):
        plt.text(i + 0.5, amplitud + 0.8, str(bit), fontsize=tamano_fuente, 
                 color='black', weight='bold', ha='center')
        
    if idx == 5:
        plt.xlabel('Tiempo (Intervalos de Bit)')
        plt.xticks(range(len(bits) + 1))
    else:
        plt.gca().set_xticklabels([])

plt.tight_layout()
plt.show()