# Projeto de Integração de Sistemas - Pipeline de Processamento de Dados

Este projeto implementa uma pipeline de processamento de dados multimédia (**Transform-Load**) utilizando Java e a biblioteca Jackson para serialização/desserialização JSON.

## Arquitetura da Pipeline

A pipeline foi desenhada para processar um objeto `Payload` (gerado automaticamente) através de uma sequência de serviços, onde cada serviço recebe um pacote de bytes, processa-o e passa-o para o seguinte.

## Lógica de Processamento nos Serviços

Como todos os serviços recebem o **mesmo pacote de bytes original**, cada um segue este fluxo interno:
1.  **DESSERIALIZAÇÃO**: O serviço converte o `byte[]` novamente para o objeto `Payload` usando o `ObjectMapper`.
2.  **FILTRAGEM/PROCESSAMENTO**: O serviço extrai e processa apenas os dados que lhe competem (Ex: `AudioService` foca-se nos `audio_samples`).
3.  **SERIALIZAÇÃO**: Após o processamento (mesmo que simulado), o serviço volta a serializar o objeto para `byte[]` para manter a interface de saída, embora na pipeline atual o estado original seja preservado para o serviço seguinte.

### Fluxo de Execução:
1.  **Encoder**: Converte o objeto Java `Payload` inicial num array de bytes (`byte[]`).
2.  **AudioService**: Processa os `audio_samples` (List<Double>) presentes em cada frame.
3.  **VideoService**: Processa os dados de `pixels` (List<Integer>) presentes em cada frame.
4.  **MetadataService**: Processa os metadados (List<Double>) associados a cada frame.
5.  **DataCollector**: Recebe o pacote final, valida a integridade dos dados e recolhe métricas de finalização.

## Estrutura do Projeto

*   `pt.uc.eai.model`: Contém as classes de dados (`Payload`, `Chunk`, `Frame`).
*   `pt.uc.eai.services`: Implementação dos serviços de processamento e codificação.
*   `pt.uc.eai.pipeline`: Orquestração do fluxo (`PipelineRunner`) e recolha de resultados (`DataCollector`).
*   `pt.uc.eai.generator`: Gerador aleatório de dados para teste.

## Como Executar

O projeto utiliza Maven. Para compilar e executar a pipeline completa, utilize (dentro de `first_assignment/`):

```bash
mvn compile exec:java -Dexec.mainClass="pt.uc.eai.Main"
```

## Configurações

As definições do gerador (número de chunks, frames por chunk, etc.) podem ser ajustadas no ficheiro:
`src/main/resources/config.properties`

---
**Nota**: O projeto foi configurado com um volume de dados moderado por defeito para garantir a execução estável em ambientes locais.
