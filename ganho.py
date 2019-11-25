def ganho(taxa, total, mes):
     ganho = 0
     salva_ganho = []
     for i in range(12):
         total = total - mes
         ganho = ganho + total*taxa
         salva_ganho.append(ganho)
     return salva_ganho


print(ganho(0.01, 1099.9, 109.99))
