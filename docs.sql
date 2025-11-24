INSERT INTO step_types (id, name, description)
VALUES
    (1, 'LOGIN_PORTAL', 'Acessar portal do cliente'),
    (2, 'BREAK_CAPTCHA', 'Quebrar captcha caso aparece na pagina'),
    (3, 'EXTRACT_DATA_PAGES', 'Extrair dados da pagina do pedido'),
    (4, 'CREATED_PAY', 'Criando datas de pagamento inicio-até'),
    (5, 'CREATED_ORDERS', 'Criando pedido vinculado com a data de pagamentos'),
    (6, 'CREATED_PRODUCTS', 'Criando os produtos com vinculo ao pedido'),
    (7, 'CREATED_TAX', 'Criar uma tax para vincular ao produto especifico')

INSERT INTO bots (id, name, description, status)
VALUES
    (1, 'Comercial - Extrair Pedidos', 'Extração dos pedidos do portal COUPA', TRUE),
    (2, 'Comercial - Gerenciar Pedido', 'Gerenciamento de Pedidos no SUPRA', FALSE);


INSERT INTO status_robot (id, description)
VALUES
    (1, 'Sucesso'),
    (2, 'Erro'),
    (3, 'Pendente');
