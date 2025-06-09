import os
from sequence import Sequence
from sequence_alignment import SequenceAlignment
from sequence_database import SequenceDatabase
from lcs_finder import LCSFinder
from lcs_finder_n_sequences import LCSFinderNSequences
from visualize import Visualize

def main():
    sequence_db = SequenceDatabase()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela do terminal
        if not sequence_db.database.values():
            print("Identificação e Análise de Regiões Genéticas Conservadas usando Subsequências Comuns Mais Longas\n")
            print("=" * 100, "\n")
            print("Selecione uma das opções abaixo:\n")
            print("> 1. Adicionar sequencia para análise")
            print("> 2. Carregar sequências de um arquivo FASTA")
            print("> 3. Sair do programa")
        else:
            print("Sequencias adicionadas:\n")
            [print(seq) for seq in sequence_db.database.values()]
            print("=" * 100, "\n")
            print("Selecione uma das opções abaixo:\n")
            print("> 1. Adicionar sequencia para análise")
            print("> 2. Carregar sequências de um arquivo FASTA")
            print("> 3. Calcular LCS entre as sequências")
            print("> 4. Exibir detalhes do alinhamento")
            print("> 5. Visualização do LCS e alinhamento")
            print("> 6. Remover sequências")
            print("> 7. Sair do programa")
        option = input(": ")
        if option == "1":
            print("")
            seq_id = input("Digite o ID da sequência: ")
            description = input("Digite a descrição da sequência: ")
            sequence = input("Digite a sequência: ")
            seq1 = Sequence(seq_id, description, sequence.upper())
            sequence_db.add_sequence(seq1)
            continue
        elif option == "2":
            print("")
            filename = input("Digite o caminho do arquivo FASTA: ")
            if not os.path.isfile(fr"{filename}"):
                print("Arquivo não encontrado. Por favor, verifique o caminho e tente novamente.\n")
                input("Pressione Enter para continuar...")
                continue
            try:
                sequence_db.load_from_fasta(fr"{filename}")
                print(f"\n{len(sequence_db.database.items())} sequências carregadas com sucesso do arquivo {fr"{filename}"}.\n")
                input("Pressione Enter para continuar...")
            except Exception as e:
                print(f"Erro ao carregar o arquivo: {e}\n")
                input("Pressione Enter para continuar...")
                continue
        elif option == "3" and len(sequence_db.database.values()) > 0:
            print("")
            if len(sequence_db.database.values()) < 2:
                print("Adicione pelo menos duas sequências para calcular o LCS.\n")
                input("Pressione Enter para continuar...")
                continue
            if len(sequence_db.database.values()) == 2:  
                seq1 = list(sequence_db.database.values())[0]
                seq2 = list(sequence_db.database.values())[1]
                lcs_finder = LCSFinder(seq1, seq2)
                print(f"Tamanho do LCS entre as sequências: {lcs_finder.get_lcs_length()}")
                print(f"LCS entre as sequências: {lcs_finder.get_lcs()}\n")
            elif len(sequence_db.database.values()) == 3:
                seq1 = list(sequence_db.database.values())[0]
                seq2 = list(sequence_db.database.values())[1]
                seq3 = list(sequence_db.database.values())[2]
                lcs_finder = LCSFinder(seq1, seq2, seq3)
                print(f"Tamanho do LCS entre as sequências: {lcs_finder.get_lcs_length()}")
                print(f"LCS entre as sequências: {lcs_finder.get_lcs()}\n")
            else:
                lcs_finder = LCSFinderNSequences(list(sequence_db.database.values()))
                print(f"Tamanho da LCS entre as sequências: {lcs_finder.get_lcs_length()}")
                print(f"LCS entre as sequências: {lcs_finder.get_lcs()}\n")
            input("Pressione Enter para continuar...")
        elif option == "4" and len(sequence_db.database.values()) > 0:
            print("")
            if len(sequence_db.database.values()) < 2:
                print("Adicione pelo menos duas sequências para exibir os detalhes do alinhamento.\n")
                input("Pressione Enter para continuar...")
                continue
            if len(sequence_db.database.values()) == 2:  
                seq1 = list(sequence_db.database.values())[0]
                seq2 = list(sequence_db.database.values())[1]
                lcs_finder = LCSFinder(seq1, seq2)
                alignment = lcs_finder.compute_lcs()
                print("Detalhes do Alinhamento:")
                print(alignment)
            elif len(sequence_db.database.values()) == 3:
                seq1 = list(sequence_db.database.values())[0]
                seq2 = list(sequence_db.database.values())[1]
                seq3 = list(sequence_db.database.values())[2]
                lcs_finder = LCSFinder(seq1, seq2, seq3)
                alignment = lcs_finder.compute_lcs()
                print("Detalhes do Alinhamento:")
                print(alignment)
            else:
                print("Para mais de 3 sequências, o alinhamento não está implementado.\n")
                input("Pressione Enter para continuar...")
                continue
            input("Pressione Enter para continuar...")
        elif option == "5" and len(sequence_db.database.values()) > 0:
            print("")
            if len(sequence_db.database.values()) < 2:
                print("Adicione pelo menos duas sequências para visualizar o LCS e o alinhamento.\n")
                input("Pressione Enter para continuar...")
                continue
            if len(sequence_db.database.values()) == 2:  
                view = Visualize(sequence_db)
                view.visualize_sequences()
            elif len(sequence_db.database.values()) == 3:
                view = Visualize(sequence_db)
                view.visualize_sequences()
            else:
                print("Para mais de 3 sequências, a visualização do LCS não está implementada.\n")
                input("Pressione Enter para continuar...")
                continue
            input("Pressione Enter para continuar...")
        elif option == "6" and len(sequence_db.database.values()) > 0:
            print("")
            print("Selecione a sequência a ser removida:")
            for i, seq in enumerate(sequence_db.database.values(), start=1):
                print(f"{i}. {seq.id} - {seq.description}")
            print(f"{len(sequence_db.database.values()) + 1}. Cancelar")
            choice = input(": ")
            if 1 <= int(choice) <= len(sequence_db.database.values()):
                print(f"\nSequência {list(sequence_db.database.keys())[int(choice) - 1]} removida.\n")
                sequence_db.remove_sequence(list(sequence_db.database.keys())[int(choice) - 1])
            elif choice == str(len(sequence_db.database.values()) + 1):
                continue
            else:
                print("Opção inválida. Nenhuma sequência foi removida.\n")
            input("Pressione Enter para continuar...")
        elif option == "7" or option == "3" and len(sequence_db.database.values()) == 0:
            print("")
            print("Saindo do programa...")
            break
        else:
            print("")
            print("Opção inválida. Por favor, selecione uma opção válida.\n")
            input("Pressione Enter para continuar...")
            continue

if __name__ == "__main__":
    main()

