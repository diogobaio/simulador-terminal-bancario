from datetime import datetime
from typing import List, Optional
import random


class Transacao:
    """Representa uma única transação"""

    def __init__(self, tipo_trans: str, valor: float, saldo: float):
        self.tipo_trans = tipo_trans
        self.valor = valor
        self.saldo = saldo
        self.data_hora = datetime.now()

    def __str__(self):
        return f"{self.data_hora.strftime('%Y-%m-%d %H:%M:%S')} | {self.tipo_trans:12} | R${self.valor:10.2f} | Saldo: R${self.saldo:10.2f}"


class Conta:
    """Classe base para conta bancária"""

    def __init__(
        self,
        numero_conta: str,
        senha: str,
        nome_titular: str,
        saldo_inicial: float = 0,
    ):
        self.numero_conta = numero_conta
        self._senha = senha
        self.nome_titular = nome_titular
        self._saldo = saldo_inicial
        self.transacoes: List[Transacao] = []
        self.conta_bloqueada = False

        if saldo_inicial > 0:
            self.transacoes.append(Transacao("ABERTURA", saldo_inicial, self._saldo))

    def verificar_senha(self, senha: str) -> bool:
        """Verificar a senha"""
        return self._senha == senha

    def alterar_senha(self, senha_antiga: str, senha_nova: str) -> bool:
        """Alterar a senha da conta"""
        if self.verificar_senha(senha_antiga):
            self._senha = senha_nova
            return True
        return False

    def obter_saldo(self) -> float:
        """Obter saldo atual"""
        return self._saldo

    def depositar(self, valor: float) -> bool:
        """Depositar dinheiro na conta"""
        if valor <= 0:
            return False
        self._saldo += valor
        self.transacoes.append(Transacao("DEPÓSITO", valor, self._saldo))
        return True

    def sacar(self, valor: float) -> bool:
        """Sacar dinheiro da conta"""
        if valor <= 0 or valor > self._saldo:
            return False
        self._saldo -= valor
        self.transacoes.append(Transacao("SAQUE", valor, self._saldo))
        return True

    def obter_historico_transacoes(self, limite: int = 10) -> List[Transacao]:
        """Obter transações recentes"""
        return self.transacoes[-limite:]

    def bloquear_conta(self):
        """Bloquear a conta"""
        self.conta_bloqueada = True

    def desbloquear_conta(self):
        """Desbloquear a conta"""
        self.conta_bloqueada = False


class ContaPoupanca(Conta):
    """Conta poupança com juros"""

    def __init__(
        self,
        numero_conta: str,
        senha: str,
        nome_titular: str,
        saldo_inicial: float = 0,
        taxa_juros: float = 0.02,
    ):
        super().__init__(numero_conta, senha, nome_titular, saldo_inicial)
        self.taxa_juros = taxa_juros

    def aplicar_juros(self):
        """Aplicar juros na conta"""
        juros = self._saldo * self.taxa_juros
        self._saldo += juros
        self.transacoes.append(Transacao("JUROS", juros, self._saldo))


class ContaCorrente(Conta):
    """Conta corrente com limite de cheque especial"""

    def __init__(
        self,
        numero_conta: str,
        senha: str,
        nome_titular: str,
        saldo_inicial: float = 0,
        limite_cheque_especial: float = 500,
    ):
        super().__init__(numero_conta, senha, nome_titular, saldo_inicial)
        self.limite_cheque_especial = limite_cheque_especial

    def sacar(self, valor: float) -> bool:
        """Saque com proteção de cheque especial"""
        if valor <= 0:
            return False
        if valor > self._saldo + self.limite_cheque_especial:
            return False
        self._saldo -= valor
        self.transacoes.append(Transacao("SAQUE", valor, self._saldo))
        return True


class Banco:
    """Sistema bancário que gerencia múltiplas contas"""

    def __init__(self, nome: str):
        self.nome = nome
        self.contas = {}

    def criar_conta(
        self, tipo_conta: str, nome_titular: str, senha: str, saldo_inicial: float = 0
    ) -> Optional[Conta]:
        """Criar uma nova conta"""
        numero_conta = self._gerar_numero_conta()

        if tipo_conta.lower() == "poupanca":
            conta = ContaPoupanca(numero_conta, senha, nome_titular, saldo_inicial)
        elif tipo_conta.lower() == "corrente":
            conta = ContaCorrente(numero_conta, senha, nome_titular, saldo_inicial)
        else:
            return None

        self.contas[numero_conta] = conta
        return conta

    def obter_conta(self, numero_conta: str) -> Optional[Conta]:
        """Recuperar uma conta"""
        return self.contas.get(numero_conta)

    def _gerar_numero_conta(self) -> str:
        """Gerar um número de conta único"""
        while True:
            numero = f"{random.randint(100000, 999999)}"
            if numero not in self.contas:
                return numero


class CaixaEletronico:
    """Interface do caixa eletrônico para operações bancárias"""

    def __init__(self, banco: Banco):
        self.banco = banco
        self.conta_atual: Optional[Conta] = None
        self.max_tentativas_senha = 3
        self.tentativas_senha = 0

    def inserir_cartao(self, numero_conta: str) -> bool:
        """Inserir cartão no caixa eletrônico"""
        conta = self.banco.obter_conta(numero_conta)
        if conta and not conta.conta_bloqueada:
            self.conta_atual = conta
            self.tentativas_senha = 0
            return True
        return False

    def verificar_senha(self, senha: str) -> bool:
        """Verificar senha com limite de tentativas"""
        if not self.conta_atual:
            return False

        if self.conta_atual.verificar_senha(senha):
            self.tentativas_senha = 0
            return True

        self.tentativas_senha += 1
        if self.tentativas_senha >= self.max_tentativas_senha:
            self.conta_atual.bloquear_conta()
            print("\n⚠️ Conta bloqueada devido a muitas tentativas falhas!")
            self.ejetar_cartao()
        return False

    def consultar_saldo(self) -> Optional[float]:
        """Consultar saldo da conta"""
        if self.conta_atual:
            return self.conta_atual.obter_saldo()
        return None

    def sacar_dinheiro(self, valor: float) -> bool:
        """Sacar dinheiro"""
        if not self.conta_atual:
            return False
        return self.conta_atual.sacar(valor)

    def depositar_dinheiro(self, valor: float) -> bool:
        """Depositar dinheiro"""
        if not self.conta_atual:
            return False
        return self.conta_atual.depositar(valor)

    def imprimir_comprovante(self):
        """Imprimir comprovante de transação"""
        if not self.conta_atual:
            return

        print("\n" + "=" * 50)
        print(f"{'COMPROVANTE CAIXA ELETRÔNICO':^50}")
        print("=" * 50)
        print(f"Banco: {self.banco.nome}")
        print(f"Conta: {self.conta_atual.numero_conta}")
        print(f"Titular: {self.conta_atual.nome_titular}")
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        print(f"Saldo Atual: R${self.conta_atual.obter_saldo():.2f}")
        print("=" * 50 + "\n")

    def mostrar_historico_transacoes(self, limite: int = 5):
        """Mostrar transações recentes"""
        if not self.conta_atual:
            return

        transacoes = self.conta_atual.obter_historico_transacoes(limite)
        print("\n" + "=" * 80)
        print(f"{'HISTÓRICO DE TRANSAÇÕES':^80}")
        print("=" * 80)
        for trans in transacoes:
            print(trans)
        print("=" * 80 + "\n")

    def ejetar_cartao(self):
        """Ejetar cartão do caixa eletrônico"""
        self.conta_atual = None
        self.tentativas_senha = 0


def exibir_menu():
    """Exibir menu do caixa eletrônico"""
    print("\n" + "=" * 40)
    print(f"{'MENU PRINCIPAL':^40}")
    print("=" * 40)
    print("1. Consultar Saldo")
    print("2. Sacar Dinheiro")
    print("3. Depositar Dinheiro")
    print("4. Histórico de Transações")
    print("5. Alterar Senha")
    print("6. Imprimir Comprovante")
    print("7. Sair")
    print("=" * 40)


def main():
    """Aplicação principal do caixa eletrônico"""
    # Inicializar banco e criar contas de exemplo
    banco = Banco("Banco Nacional Python")

    # Criar contas de exemplo
    conta1 = banco.criar_conta("poupanca", "Cristiano Ronaldo", "070707", 10000000.0)
    conta2 = banco.criar_conta("corrente", "Lionel Messi", "101010", 500000.0)

    print("=" * 50)
    print(f"{'BEM-VINDO AO BANCO NACIONAL PYTHON':^50}")
    print("=" * 50)
    print("\nContas de Exemplo Criadas:")
    print(f"Conta 1: {conta1.numero_conta} (Senha: 1234) - Poupança")
    print(f"Conta 2: {conta2.numero_conta} (Senha: 5678) - Corrente")

    # Interface do Caixa Eletrônico
    caixa = CaixaEletronico(banco)

    # Inserir cartão
    print("\n" + "-" * 50)
    numero_conta = input("Digite o número da conta: ")

    if not caixa.inserir_cartao(numero_conta):
        print("❌ Conta inválida ou conta bloqueada!")
        return

    # Verificação de senha
    for tentativa in range(3):
        senha = input("Digite a senha: ")
        if caixa.verificar_senha(senha):
            print("✅ Senha verificada com sucesso!\n")
            break
        else:
            restantes = 2 - tentativa
            if restantes > 0:
                print(f"❌ Senha incorreta. {restantes} tentativas restantes.")
    else:
        return

    # Loop do menu principal
    while True:
        exibir_menu()
        opcao = input("Selecione uma opção (1-7): ")

        if opcao == "1":
            saldo = caixa.consultar_saldo()
            print(f"\n💰 Saldo Atual: R${saldo:.2f}")

        elif opcao == "2":
            valor = float(input("Digite o valor do saque: R$"))
            if caixa.sacar_dinheiro(valor):
                print(f"✅ Saque de R${valor:.2f} realizado com sucesso!")
                print(f"💰 Novo saldo: R${caixa.consultar_saldo():.2f}")
            else:
                print("❌ Saldo insuficiente ou valor inválido!")

        elif opcao == "3":
            valor = float(input("Digite o valor do depósito: R$"))
            if caixa.depositar_dinheiro(valor):
                print(f"✅ Depósito de R${valor:.2f} realizado com sucesso!")
                print(f"💰 Novo saldo: R${caixa.consultar_saldo():.2f}")
            else:
                print("❌ Valor inválido!")

        elif opcao == "4":
            caixa.mostrar_historico_transacoes()

        elif opcao == "5":
            senha_antiga = input("Digite a senha atual: ")
            senha_nova = input("Digite a nova senha: ")
            if caixa.conta_atual.alterar_senha(senha_antiga, senha_nova):
                print("✅ Senha alterada com sucesso!")
            else:
                print("❌ Senha atual incorreta!")

        elif opcao == "6":
            caixa.imprimir_comprovante()

        elif opcao == "7":
            caixa.imprimir_comprovante()
            print("\n👋 Obrigado por utilizar o Banco Nacional Python!")
            print("Por favor, retire seu cartão.\n")
            caixa.ejetar_cartao()
            break

        else:
            print("❌ Opção inválida. Por favor, tente novamente.")


if __name__ == "__main__":
    main()
