# cosmobase-school-2026
Material for the CosmoBase cosmology school in Puebla 2026: L-PICOLA simulations, installation guides, notebooks, and large-scale structure analysis

# Carpeta doc:
-PDF Clase: formación estructura L-PICOLA
-PDF instalación paquetes
-PDF paper L-PICOLA
-PDF Guía de L-PICOLA

# Carpeta notebooks:
- tut1_density_field.ipynb   (Tutorial para campo de densidades y partículas)
- tut2_pk_hmf.ipynb          (Tutorial para P(j) y HMF:)
- calculate_fof.py           (script para generar catalogo de halos mediante fof)
- Otras carpetas

# Carpetas dentro de carpeta notebooks
- Carpeta "halos" 
  -> Contiene dos archivos de halos para z=0.5 y z=0.0 generados con nbodykit
- Carpeta "inputs_lpicola" 
  - input_spectrum.dat         (Espectro de potencia de entra)
  - output_redshifts.dat       (Snapshots generados para cada redshift y número de pasos entre ellos)
  - run_parameters_puebla.dat  (Configura los parámetros y archivos de entrada como "input_spectrum.dat" y "output_redshifts.dat")
  
# NOTA 
1.- Opcionalmente puede instalar el paquete nbodykit para utilizar el script "calculate_fof.py" para ver detalles de instalación:
https://nbodykit.readthedocs.io/en/latest/getting-started/install.html

2.- Los tutoriales son basados en los mostrados por Pylians para un suit de simulaciones llamadas QUIJOTE:
https://quijote-simulations.readthedocs.io/en/latest/tutorials.html

  
