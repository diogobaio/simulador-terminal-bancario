# 🏦 Terminal Bancário em Python

Terminal bancário implementado em Python que simula operações de caixa eletrônico, gerenciamento de contas e transações financeiras.

## 🚀 Funcionalidades

- **Criação de Contas**: Geração de conta corrente e poupança de exemplo
- **Operações Bancárias**: Saque, depósito e consulta de saldo
- **Autenticação Segura**: Sistema de senha com bloqueio após tentativas falhas
- **Histórico de Transações**: Registro completo de todas as operações
- **Juros**: Aplicação automática de juros em contas poupança
- **Cheque Especial**: Limite configurável para contas correntes
- **Comprovantes**: Geração de comprovantes de transações

## 🏗️ Arquitetura do Sistema

### Classes Principais

#### 1. **Transacao**

Classe que representa uma transação individual com:

- Data e hora automática
- Tipo de transação
- Valor envolvido
- Saldo resultante

#### 2. **Conta (Classe Base)**

Implementa a lógica básica de uma conta bancária:

- Gerenciamento de saldo
- Verificação de senha
- Histórico de transações
- Bloqueio/desbloqueio de conta

#### 3. **ContaPoupanca**

Herda de `Conta` e adiciona:

- Aplicação de juros
- Taxa de juros configurável

#### 4. **ContaCorrente**

Herda de `Conta` e implementa:

- Limite de cheque especial
- Saque com proteção contra saldo negativo excessivo

#### 5. **Banco**

Gerencia múltiplas contas:

- Criação de contas com números únicos
- Armazenamento em dicionário para acesso rápido
- Geração aleatória de números de conta

#### 6. **CaixaEletronico**

Interface do usuário com:

- Autenticação segura
- Limite de tentativas de senha
- Menu interativo
- Comprovantes de transações

## 💡 Lógica de Programação Python Utilizada

### 1. **Programação Orientada a Objetos**

```python
# Herança e polimorfismo
class ContaPoupanca(Conta):
    def aplicar_juros(self):
        # Método específico da classe derivada
        pass
```

### 2. **Encapsulamento**

```python
# Atributos privados com underscore
self._senha
self._saldo

# Métodos públicos para acesso controlado
def verificar_senha(self, senha: str) -> bool:
def obter_saldo(self) -> float:
```

### 3. **Tipagem Estática**

```python
# Type hints para melhor documentação e autocomplete
def depositar(self, valor: float) -> bool:
def obter_historico_transacoes(self, limite: int = 10) -> List[Transacao]:
```

### 4. **Gerenciamento de Estado**

```python
# Controle de tentativas de senha
self.tentativas_senha += 1
if self.tentativas_senha >= self.max_tentativas_senha:
    self.conta_atual.bloquear_conta()
```

### 5. **Manipulação de Datas**

```python
# Uso do módulo datetime
from datetime import datetime
self.data_hora = datetime.now()
```

### 6. **Estruturas de Dados**

```python
# Listas para histórico de transações
self.transacoes: List[Transacao] = []

# Dicionários para mapeamento de contas
self.contas = {}
conta = self.contas.get(numero_conta)
```

### 7. **Validação e Tratamento de Erros**

```python
# Validação de entrada
if valor <= 0 or valor > self._saldo:
    return False

# Controle de fluxo com retornos booleanos
def sacar(self, valor: float) -> bool:
```

### 8. **Geração de Números Únicos**

```python
# Algoritmo para gerar números de conta não repetidos
def _gerar_numero_conta(self) -> str:
    while True:
        numero = f"{random.randint(100000, 999999)}"
        if numero not in self.contas:
            return numero
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**
- **Módulo datetime** para registro temporal
- **Módulo random** para geração de números de conta
- **Type hints** para melhor legibilidade do código
- **Programação orientada a objetos** para organização do sistema

## 📋 Pré-requisitos

- Python 3.7 ou superior instalado
- Nenhuma dependência externa necessária

## 🚀 Como Executar

1. Clone ou copie o código para seu ambiente
2. Execute o arquivo principal:

```bash
python terminal-bancario.py
```

## 🎯 Pontos de Destaque

1. **Código Limpo**: Nomes descritivos em português, seguindo boas práticas
2. **Segurança**: Senhas nunca são exibidas, conta bloqueia após tentativas
3. **Extensibilidade**: Fácil adição de novos tipos de conta
4. **Robustez**: Validação de todas as entradas do usuário
5. **Usabilidade**: Interface intuitiva com menus claros

*Desenvolvido para fins de estudo e prática de POO com Python.*
