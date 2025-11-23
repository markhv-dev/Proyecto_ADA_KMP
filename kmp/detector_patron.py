class DetectorPatron:
    def __init__(self, patron):
        self.patron = patron
        self.lps = self._calcular_lps(patron)
        
    def _calcular_lps(self, patron):
        """Calcular el array LPS (Longest Prefix Suffix) para KMP"""
        lps = [0] * len(patron)
        longitud = 0
        i = 1
        
        while i < len(patron):
            if patron[i] == patron[longitud]:
                longitud += 1
                lps[i] = longitud
                i += 1
            else:
                if longitud != 0:
                    longitud = lps[longitud - 1]
                else:
                    lps[i] = 0
                    i += 1
                    
        return lps
        
    def detectar_patron(self, texto, ultimo_indice_detectado):
        """Buscar patrón en texto usando algoritmo KMP"""
        M = len(self.patron)
        N = len(texto)
        
        if M == 0 or N < M:
            return {"detectado": False, "nuevo": False, "indice": -1}
            
        i = 0  # índice para texto
        j = 0  # índice para patrón
        
        while i < N:
            if self.patron[j] == texto[i]:
                i += 1
                j += 1
                
            if j == M:
                indice_inicio = i - j
                # Verificar si es una nueva detección (no solapada)
                if indice_inicio > ultimo_indice_detectado:
                    return {
                        "detectado": True, 
                        "nuevo": True, 
                        "indice": indice_inicio
                    }
                j = self.lps[j - 1]
            elif i < N and self.patron[j] != texto[i]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
                    
        return {"detectado": False, "nuevo": False, "indice": -1}