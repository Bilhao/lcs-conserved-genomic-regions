import os
from sequence import Sequence
from sequence_alignment import SequenceAlignment
from sequence_database import SequenceDatabase
from lcs_finder import LCSFinder
from lcs_finder_n_sequences import LCSFinderNSequences

def main():
    sequences = []
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela do terminal
        if not sequences:
            print("Identificação e Análise de Regiões Genéticas Conservadas usando Subsequências Comuns Mais Longas\n")
            print("=" * 100, "\n")
            print("Selecione uma das opções abaixo:\n")
            print("> 1. Adicionar sequencia para análise")
            print("> 2. Carregar sequências de um arquivo FASTA")
            print("> 3. Sair do programa")
        else:
            print("Sequencias adicionadas:\n")
            [print(seq) for seq in sequences]
            print("=" * 100, "\n")
            print("Selecione uma das opções abaixo:\n")
            print("> 1. Adicionar sequencia para análise")
            print("> 2. Carregar sequências de um arquivo FASTA")
            print("> 3. Calcular LCS entre as sequências")
            print("> 4. Exibir detalhes do alinhamento")
            print("> 5. Visualização do LCS e alinhamento")
            print("> 6. Sair do programa")
        option = input(": ")
        if option == "1":
            print("")
            seq_id = input("Digite o ID da sequência: ")
            description = input("Digite a descrição da sequência: ")
            sequence = input("Digite a sequência: ")
            seq1 = Sequence(seq_id, description, sequence.upper())
            sequences.append(seq1)
            continue
        elif option == "2":
            print("")
            print("Opção 2 selecionada. Carregando sequências de um arquivo FASTA...")
        elif option == "3" and len(sequences) > 0:
            print("")
            if len(sequences) < 2:
                print("Por favor, adicione pelo menos duas sequências para calcular o LCS.")
                input("Pressione Enter para continuar...")
                continue
            if len(sequences) == 2:  
                seq1 = sequences[0]
                seq2 = sequences[1]
                lcs_finder = LCSFinder(seq1, seq2)
                print(f"Tamanho do LCS entre as sequências: {lcs_finder.get_lcs_length()}")
                print(f"LCS entre as sequências: {lcs_finder.get_lcs()}")
            elif len(sequences) == 3:
                seq1 = sequences[0]
                seq2 = sequences[1]
                seq3 = sequences[2]
                lcs_finder = LCSFinder(seq1, seq2, seq3)
                print(f"Tamanho do LCS entre as sequências: {lcs_finder.get_lcs_length()}")
                print(f"LCS entre as sequências: {lcs_finder.get_lcs()}")
            else:
                lcs_finder = LCSFinderNSequences(sequences)
                print(f"Tamanho da LCS entre as sequências: {lcs_finder.get_lcs_length()}")
                print(f"LCS entre as sequências: {lcs_finder.get_lcs()}")
            input("Pressione Enter para continuar...")
        elif option == "4":
            print("")
            if len(sequences) < 2:
                print("Por favor, adicione pelo menos duas sequências para exibir os detalhes do alinhamento.")
                input("Pressione Enter para continuar...")
                continue
            if len(sequences) == 2:  
                seq1 = sequences[0]
                seq2 = sequences[1]
                lcs_finder = LCSFinder(seq1, seq2)
                alignment = lcs_finder.compute_lcs()
                print("Detalhes do Alinhamento:")
                print(alignment)
            elif len(sequences) == 3:
                seq1 = sequences[0]
                seq2 = sequences[1]
                seq3 = sequences[2]
                lcs_finder = LCSFinder(seq1, seq2, seq3)
                alignment = lcs_finder.compute_lcs()
                print("Detalhes do Alinhamento:")
                print(alignment)
            else:
                print("Para mais de 3 sequências, o alinhamento não está implementado.")
                input("Pressione Enter para continuar...")
                continue
            input("Pressione Enter para continuar...")
        elif option == "5":
            print("")
            if len(sequences) < 2:
                print("Por favor, adicione pelo menos duas sequências para visualizar o LCS e o alinhamento.")
                input("Pressione Enter para continuar...")
                continue
            if len(sequences) == 2:  
                seq1 = sequences[0]
                seq2 = sequences[1]
                lcs_finder = LCSFinder(seq1, seq2)
                lcs_finder.visualize()
            elif len(sequences) == 3:
                seq1 = sequences[0]
                seq2 = sequences[1]
                seq3 = sequences[2]
                lcs_finder = LCSFinder(seq1, seq2, seq3)
                lcs_finder.visualize()
            else:
                print("Para mais de 3 sequências, a visualização do LCS não está implementada.")
                input("Pressione Enter para continuar...")
                continue
            input("Pressione Enter para continuar...")
        elif option == "6" or option == "3" and len(sequences) == 0:
            print("")
            print("Saindo do programa...")
            break
        else:
            print("")
            print("Opção inválida. Por favor, selecione uma opção válida.")
            input("Pressione Enter para continuar...")
            continue

if __name__ == "__main__":
    main()

