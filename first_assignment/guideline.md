# Guia de Execução - Payload Generator (IS)

Este guia descreve como compilar e executar o gerador de payloads para testes de performance (JSON).

## Como Rodar

### 🚀 Forma Simples (Recomendada)
Para volumes de dados normais (até 100k registos), usa o comando simplificado dentro da pasta `first_assignment`:

```bash
mvn compile exec:java
```

### 📝 Forma Alternativa  
Se preferires especificar a classe principal explicitamente:

```bash
mvn compile exec:java -Dexec.mainClass="pt.uc.eai.Main"
```

---

## Erro: `OutOfMemoryError: Java heap space`

Ao tentar gerar volumes elevados (ex: 1.000.000 de dados), o Java pode ficar sem memória RAM disponível por defeito.

### Como Resolver:
Deves aumentar o limite de memória da JVM antes de rodar o Maven. No terminal (macOS/Linux), executa:

```bash
export MAVEN_OPTS="-Xmx2g"
mvn compile exec:java
```

Para Windows (PowerShell), usa:
```powershell
$env:MAVEN_OPTS="-Xmx2g"
mvn compile exec:java
```

*Nota: Estas configurações só são válidas para a sessão atual do terminal.*

---

## Estatísticas
- Os resultados de cada execução (tempo de serialização e tamanho do ficheiro) são guardados automaticamente no ficheiro `stats.csv`.
- O payload gerado é gravado no ficheiro definido em `src/main/resources/config.properties`.

## Configuração

### 📊 Alternar entre JSON e BSON
Para comparar performance entre formatos, edita o ficheiro `src/main/resources/config.properties`:

```properties
# FORMATO DE SERIALIZAÇÃO: JSON ou BSON
serialization.format=JSON   # Para teste JSON
# serialization.format=BSON  # Para teste BSON
```

### 📈 Análise de Resultados  
- Execute primeiro com `serialization.format=JSON`
- Execute depois com `serialization.format=BSON` 
- Compare os resultados no ficheiro `stats.csv` (coluna Format)

### 📝 Outras Configurações
Para alterar o volume de dados ou a `seed`, edita o ficheiro:
`src/main/resources/config.properties`
