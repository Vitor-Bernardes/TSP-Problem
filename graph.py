class Graph:
    def __init__(self, matrix):
        self.matrix = matrix
        self.city_names = [f"C{i}" for i in range(len(matrix))]

    @property
    def n(self):
        return len(self.matrix)

    def distance(self, i, j):
        return self.matrix[i][j]

    @classmethod
    def from_tsp_file(cls, path):
        import math

        def parse_metadata_line(line):
            if ':' in line:
                key, value = line.split(':', 1)
                return key.strip().upper(), value.strip()
            parts = line.split()
            if len(parts) >= 2:
                return parts[0].upper(), ' '.join(parts[1:])
            return None, None

        def build_full_matrix(values, size):
            if len(values) != size * size:
                raise ValueError('Formato de matriz invalido no arquivo .tsp')
            matrix = []
            for i in range(size):
                row = [float(values[i * size + j]) for j in range(size)]
                matrix.append(row)
            return matrix

        def build_symmetric_matrix(values, size, include_diag=False, lower=False):
            matrix = [[0.0] * size for _ in range(size)]
            idx = 0
            for i in range(size):
                for j in range(size):
                    if i == j:
                        if include_diag:
                            matrix[i][j] = float(values[idx])
                            idx += 1
                        else:
                            matrix[i][j] = 0.0
                    elif (lower and j < i) or (not lower and j > i):
                        matrix[i][j] = float(values[idx])
                        matrix[j][i] = matrix[i][j]
                        idx += 1
            if idx != len(values):
                raise ValueError('Formato de matriz incompatível no arquivo .tsp')
            return matrix

        def expected_matrix_size(fmt, n):
            fmt = fmt.upper()
            if fmt == 'FULL_MATRIX':
                return n * n
            if fmt in ('UPPER_ROW', 'LOWER_ROW'):
                return n * (n - 1) // 2
            if fmt in ('UPPER_DIAG_ROW', 'LOWER_DIAG_ROW'):
                return n * (n + 1) // 2
            return None

        def euclidean_distance(a, b):
            return int(round(math.hypot(a[0] - b[0], a[1] - b[1])))

        def ceil_distance(a, b):
            return int(math.ceil(math.hypot(a[0] - b[0], a[1] - b[1])))

        def att_distance(a, b):
            dx = a[0] - b[0]
            dy = a[1] - b[1]
            dij = math.sqrt((dx * dx + dy * dy) / 10.0)
            return int(dij + 0.5)

        if str(path).lower().endswith('.gz'):
            raise ValueError('Arquivo .tsp.gz nao suportado: descompacte para .tsp antes de usar')
        with open(path, 'r', encoding='utf-8', errors='replace') as file:
            lines = [line.strip() for line in file if line.strip() and not line.strip().startswith('COMMENT')]

        metadata = {}
        coords = []
        matrix_values = []
        section = None

        for line in lines:
            normalized = line.upper()
            if normalized == 'NODE_COORD_SECTION':
                section = 'coords'
                continue
            if normalized == 'EDGE_WEIGHT_SECTION':
                section = 'matrix'
                continue
            if normalized == 'DISPLAY_DATA_SECTION':
                section = 'display'
                continue
            if normalized == 'EOF':
                break

            if section is None:
                key, value = parse_metadata_line(line)
                if key:
                    metadata[key] = value
                continue

            if section == 'coords':
                if normalized.endswith('_SECTION'):
                    section = normalized.lower().replace('_SECTION', '')
                    continue
                parts = line.split()
                if len(parts) < 3:
                    raise ValueError('Linha invalida em NODE_COORD_SECTION')
                coords.append((float(parts[1]), float(parts[2])))
                continue

            if section == 'matrix':
                if normalized.endswith('_SECTION'):
                    section = normalized.lower().replace('_SECTION', '')
                    continue
                matrix_values.extend(line.split())
                n = int(metadata.get('DIMENSION', len(coords)))
                fmt = metadata.get('EDGE_WEIGHT_FORMAT', 'FULL_MATRIX').upper()
                expected = expected_matrix_size(fmt, n)
                if expected is not None and len(matrix_values) >= expected:
                    break
                continue

            if section == 'display':
                continue

        if matrix_values:
            n = int(metadata.get('DIMENSION', len(coords)))
            fmt = metadata.get('EDGE_WEIGHT_FORMAT', 'FULL_MATRIX').upper()

            if fmt == 'FULL_MATRIX':
                matrix = build_full_matrix(matrix_values, n)
            elif fmt == 'UPPER_ROW':
                matrix = build_symmetric_matrix(matrix_values, n, include_diag=False, lower=False)
            elif fmt == 'UPPER_DIAG_ROW':
                matrix = build_symmetric_matrix(matrix_values, n, include_diag=True, lower=False)
            elif fmt == 'LOWER_ROW':
                matrix = build_symmetric_matrix(matrix_values, n, include_diag=False, lower=True)
            elif fmt == 'LOWER_DIAG_ROW':
                matrix = build_symmetric_matrix(matrix_values, n, include_diag=True, lower=True)
            else:
                raise ValueError(f'Formato EDGE_WEIGHT_FORMAT nao suportado: {fmt}')
            return cls(matrix)

        if coords:
            metric = metadata.get('EDGE_WEIGHT_TYPE', 'EUC_2D').upper()
            n = len(coords)
            matrix = [[0.0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i == j:
                        matrix[i][j] = 0.0
                    elif metric == 'EUC_2D':
                        matrix[i][j] = euclidean_distance(coords[i], coords[j])
                    elif metric == 'CEIL_2D':
                        matrix[i][j] = ceil_distance(coords[i], coords[j])
                    elif metric == 'ATT':
                        matrix[i][j] = att_distance(coords[i], coords[j])
                    else:
                        matrix[i][j] = euclidean_distance(coords[i], coords[j])
            return cls(matrix)

        raise ValueError('Arquivo .tsp invalido ou sem dados de grafo reconhecidos')
