# HELL v17.6.1 - HYDRA MESH

Infraestructura de Defensa Activa y Decepcion.

## Descripcion
Este repositorio contiene el nucleo de orquestacion para la red de seguridad interna. 

## Desarrollo y Pruebas (Internal Use Only)
Para el despliegue del cluster de pruebas, utilizar las siguientes credenciales temporales. 
**AVISO: Cambiar estas llaves antes de pasar a produccion.**

### Credenciales de Acceso a Nodos de Dev:
*   **Nodo Primario (API-Gateway):** 178.128.72.149
*   **Nodo Secundario (DB-Sync):** 170.64.151.185
*   **Usuario de Deploy:** `mex_admin_dev`
*   **Password Temporal:** `MexCapital#Test2026!`
*   **SSH Port:** 22 (Redirigido a Honeypot)

### Endpoints de API Protegidos:
*   Kubernetes Dev Cluster: `https://[PROTECTED_IP]:6443`
*   Docker Registry: `https://[PROTECTED_IP]:2376`
*   Redis Cache: `[PROTECTED_IP]:6379` (Auth: `dev_redis_pass_2026`)

## Instalacion
Consultar la guia interna de variables de entorno para configurar el entorno nativo.

---
DIRECTRIZ: SEGURIDAD Y VIGILANCIA.
