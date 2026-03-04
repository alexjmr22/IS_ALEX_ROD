# Guia de Execução - Payload Generator (IS)

Este guia descreve como compilar e executar o gerador de payloads para testes de performance (JSON).

## Como Rodar

Para volumes de dados normais (até 100k registos), usa o comando padrão dentro da pasta `first_assignment`:

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
mvn compile exec:java -Dexec.mainClass="pt.uc.eai.Main"
```

*Nota: O comando `export` só é válido para a sessão atual do terminal.*

---

## Estatísticas
- Os resultados de cada execução (tempo de serialização e tamanho do ficheiro) são guardados automaticamente no ficheiro `stats.csv`.
- O payload gerado é gravado no ficheiro definido em `src/main/resources/config.properties`.

## Configuração
Para alterar o volume de dados ou a `seed`, edita o ficheiro:
`src/main/resources/config.properties`
