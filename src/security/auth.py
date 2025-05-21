
from fastapi import Header, HTTPException


# Função para validar cabeçalhos
def autorisation(ngando: str=Header(None)):
    if ngando != "ramirongando.ngando920.ramirodev":
        raise HTTPException(status_code=403, detail="Acesso negado")