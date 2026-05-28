from uuid import UUID


class Usuario:

    def __init__(
        self,
        usuario_id: UUID,
        usuario_nombre: str,
        usuario_email: str,
        usuario_telefono: str,
        usuario_activo: bool,
        usuario_familiar_nombre: str,
        usuario_familiar_telefono: str
    ):

        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre
        self.usuario_email = usuario_email
        self.usuario_telefono = usuario_telefono
        self.usuario_activo = usuario_activo

        self.usuario_familiar_nombre = usuario_familiar_nombre
        self.usuario_familiar_telefono = usuario_familiar_telefono

    def registrar(self):

        print("Usuario registrado")

    def iniciar_sesion(self):

        print("Sesión iniciada")