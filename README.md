# 🤖 Laboratorios de Robótica: Modelado, Control y Navegación en ROS 2

Bienvenido al repositorio oficial de las prácticas de laboratorio del curso de **Robótica**. Este espacio recopila el desarrollo experimental, los códigos fuente y los informes técnicos orientados al estudio de la cinemática, el control de robots móviles, el mapeo (SLAM) y la navegación autónoma.

---

## 👥 Autores
* **Juan Simón Jaramillo Henao**
* **Rafael Montoya Pineda**

**Institución:** Universidad Nacional de Colombia - Sede Manizales  
**Facultad:** Ingeniería y Arquitectura  

---

## 🛠️ Herramientas y tecnologías
Los laboratorios están desarrollados utilizando el siguiente ecosistema tecnológico:
* **Lenguajes:** Python 3, \LaTeX (para documentación técnica).
* **Librerías Matemáticas:** `numpy`, `scipy` (`scipy.spatial.transform`), `matplotlib`, `roboticstoolbox-python`.
* **Middleware:** ROS 2 (Jazzy / Humble).
* **Simulación y visualización:** Gazebo, RViz2, TF2.
* **Plataforma robótica:** TurtleBot3 (Modelo Burger).
* **Stacks de navegación:** Cartographer (SLAM), Navigation 2 (Nav2).

---

## 📂 Estructura del repositorio y laboratorios

El repositorio está organizado en carpetas independientes para cada laboratorio. A continuación se describe el progreso actual del curso:

### ✅ Laboratorios completados

* **[Laboratorio 1](./Laboratorio_1):** Introducción al entorno de simulación y herramientas básicas de ROS 2. *(Añadir detalles si es necesario)*
* **[Laboratorio 2](./Laboratorio_2): Representación de Pose y Cuaterniones.**
  * Uso de matrices de rotación y cuaterniones (SO(3) y SE(3)).
  * Interpolación esférica (SLERP) y árboles de transformación con TF2.
* **[Laboratorio 3](./Laboratorio_3): Movimiento, Velocidad y Trayectorias.**
  * Integración discreta de odometría e IMU.
  * Generación y evaluación de trayectorias (Quíntica y Trapezoidal).
* **[Laboratorio 4](./Laboratorio_4): Modelado Cinemático y Control en Lazo Cerrado.**
  * Simulación del modelo cinemático tipo bicicleta.
  * Leyes de control: ir a un punto, seguimiento de línea y *Pure Pursuit*.
  * Integración de comandos cinemáticos en Gazebo con el TurtleBot3.
* **[Laboratorio 5](./Laboratorio_5): De lo Reactivo a la Navegación Global (Nav2).**
  * **Navegación Reactiva y Búsqueda:** Vehículo de Braitenberg, Bug2, A* y Transformada de Distancia.
  * **SLAM:** Mapeo de ocupación con Cartographer.
  * **Navegación Autónoma:** Localización con AMCL, mapas de costo, conductas de recuperación (*recoveries*) y evasión de obstáculos con Nav2.

### 🚀 Próximos laboratorios (En desarrollo)

* **[Laboratorio 6](./Laboratorio_6):** *[Espacio reservado para el próximo laboratorio.]*
* **[Laboratorio 7](./Laboratorio_7):** *[Espacio reservado para el próximo laboratorio.]*
