# Guía de Seguridad - Herramientas PromiTierra

## Verificación de Autenticidad

Para garantizar que está utilizando una versión auténtica y segura de Herramientas PDF PromiTierra, siga estos pasos:

1. **Fuente de Descarga**
   - Descargue el software ÚNICAMENTE desde nuestro repositorio de github ofici: https://github.com/promitierra/tools-promitierra/releases
   - NO descargue el software de sitios de terceros o enlaces no oficiales

2. **Verificación de Firma Digital**
   - Haga clic derecho en el archivo ejecutable
   - Seleccione "Propiedades"
   - Vaya a la pestaña "Firmas digitales"
   - Verifique que:
     - El certificado esté emitido a "PromiTierra"
     - La firma sea válida y de confianza
     - No haya advertencias de seguridad

3. **Verificación de Hash**
   - Compare el hash SHA-256 del archivo descargado con el publicado en nuestra página oficial
   - Puede generar el hash usando PowerShell:
     ```powershell
     Get-FileHash -Algorithm SHA256 HerramientasPDF.exe | Format-List
     ```

## Advertencias de Seguridad

### Advertencias Normales
Es normal que al descargar o ejecutar por primera vez el programa, Windows SmartScreen muestre una advertencia. Esto ocurre porque:
- Somos un publicador nuevo
- El software no tiene un historial extenso de descargas

Para proceder de forma segura:
1. Verifique que ha descargado el archivo de nuestra fuente oficial
2. Verifique la firma digital como se indicó anteriormente
3. Haga clic en "Más información" en la advertencia de SmartScreen
4. Seleccione "Ejecutar de todos modos"

### Advertencias Preocupantes
Debe preocuparse si:
- El archivo no tiene firma digital
- La firma digital no corresponde a PromiTierra
- Su antivirus detecta el archivo como malicioso
- El hash no coincide con el publicado oficialmente

En estos casos, NO ejecute el archivo y contacte nuestro soporte técnico.

## Preguntas Frecuentes

### ¿Por qué Windows muestra una advertencia?
Windows SmartScreen muestra advertencias para software nuevo o poco común como medida de seguridad. Una vez que el software tenga más descargas y reputación, estas advertencias disminuirán.

### ¿Es seguro ignorar la advertencia de SmartScreen?
Sí, siempre y cuando:
- Haya descargado el software de nuestra fuente oficial
- Haya verificado la firma digital
- El hash coincida con el publicado

### ¿Por qué necesitan tantos permisos?
El software requiere permisos para:
- Leer/escribir archivos PDF
- Acceder a la memoria para procesamiento
- Crear archivos temporales
No solicitamos ni utilizamos más permisos que los estrictamente necesarios.

### ¿Cómo reporto un problema de seguridad?
Si encuentra un problema de seguridad:
1. No comparta el problema públicamente
2. Envíe un reporte detallado a nuestro equipo de seguridad
3. Incluya pasos para reproducir el problema
4. Adjunte evidencia si es posible

## Actualizaciones de Seguridad

- Las actualizaciones se publican automáticamente en nuestra página oficial
- Cada actualización incluye su propia firma digital y hash
- Recomendamos mantener el software actualizado
- Las actualizaciones de seguridad críticas se notifican por correo electrónico

## Contacto

Para reportar problemas de seguridad o verificar la autenticidad del software:
- Email: contacto@promitierra.com
- Teléfono: +57 311 612 4993
- Horario: Lunes a Viernes, 9:00 - 18:00 