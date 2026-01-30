# Exporta funções do client_service para importação mais fácil
from .client_service import (
    get_client,
    get_clients,
    create_client,
    update_client,
    delete_client,
    deactivate_client
)
# Exporta funções do product_service
from .product_service import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product
)