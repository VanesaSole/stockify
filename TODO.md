# TODO - Sitio web con login/registro/recuperación (FastAPI + Jinja2)

- [ ] Crear estructura de proyecto web (carpeta `web/` con subcarpetas core/db/routes/schemas/services/templates/static).
- [ ] Implementar base de datos SQLite + SQLAlchemy (models + session manager).
- [ ] Implementar autenticación:
  - [ ] Registro (nombre, mail, pass + confirmación, dirección, teléfono).
  - [ ] Login (mail + contraseña).
- [ ] Implementar recuperación de contraseña:
  - [ ] Endpoint “Olvidé mi contraseña” (ingreso de mail).
  - [ ] Generar token, guardarlo en DB, expirar y enviar link.
  - [ ] Página formulario de reset por token.
  - [ ] Actualizar contraseña.
- [ ] Implementar seguridad:
  - [ ] Hash de contraseñas (bcrypt/argon2).
  - [ ] JWT o cookie de sesión.
  - [ ] Validaciones (email único, confirmación de contraseña, etc.).
- [ ] Crear plantillas Jinja2: login.html, register.html, forgot_password.html, reset_password.html.
- [ ] Crear rutas FastAPI que rendericen templates y manejen POST.
- [ ] Crear un `requirements.txt` y documento de ejecución (run locally).
- [ ] Probar flujos: registro -> login -> forgot -> reset -> login.

