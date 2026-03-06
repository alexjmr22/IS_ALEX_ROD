package pt.uc.eai.pipeline;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;

import pt.uc.eai.Config;
import pt.uc.eai.model.Payload;
import pt.uc.eai.model.ServiceMetrics;
import pt.uc.eai.services.AudioService;
import pt.uc.eai.services.Encoder;
import pt.uc.eai.services.MetadataService;
import pt.uc.eai.services.VideoService;

public class PipelineRunner {

    private final Encoder encoder;
    private final AudioService audioService;
    private final VideoService videoService;
    private final MetadataService metadataService;
    private final DataCollector dataCollector;
    private final String serializationFormat;

    public PipelineRunner(ObjectMapper mapper) {
        this.encoder = new Encoder(mapper);
        this.audioService = new AudioService(mapper);
        this.videoService = new VideoService(mapper);
        this.metadataService = new MetadataService(mapper);
        this.dataCollector = new DataCollector(mapper);
        
        // Detectar formato baseado no tipo de ObjectMapper
        this.serializationFormat = (mapper.getFactory().getClass().getSimpleName().contains("Bson")) ? "BSON" : "JSON";
    }

    public void run(Payload initialPayload) {
        int iterations = Integer.parseInt(Config.getProperty("pipeline.iterations", "1"));
        System.out.println("Iniciando Pipeline (Config Iteration: " + iterations + "x) com Métricas: Encoder -> AudioService -> VideoService -> MetadataService -> DataCollector");

        // Map para acumular somas das métricas por serviço
        Map<String, ServiceMetricsAccumulator> accumulators = new HashMap<>();

        try {
            for (int i = 0; i < iterations; i++) {
                if (iterations > 1) {
                    System.out.println("Executando iteração " + (i + 1) + "/" + iterations + "...");
                }

                // 1. Encoder
                byte[] originalPacket = encoder.encode(initialPayload);
                
                // 2. AudioService
                audioService.process(originalPacket);
                
                // 3. VideoService
                videoService.process(originalPacket);
                
                // 4. MetadataService
                metadataService.process(originalPacket);

                // Acumular métricas desta iteração
                accumulate(accumulators, audioService.getMetrics());
                accumulate(accumulators, videoService.getMetrics());
                accumulate(accumulators, metadataService.getMetrics());
            }

            // Calcular médias
            List<ServiceMetrics> averagedMetrics = new ArrayList<>();
            for (ServiceMetricsAccumulator acc : accumulators.values()) {
                averagedMetrics.add(new ServiceMetrics(
                    acc.serviceName,
                    acc.totalDeTime / iterations,
                    acc.totalSeTime / iterations,
                    acc.totalTime / iterations,
                    acc.messageSize,
                    acc.totalRAM / iterations
                ));
            }

            // Identificador baseado no nome do ficheiro ou configuração ativa
            String payloadId = Config.getProperty("generator.nameFile", "unknown_payload");

            // 5. DataCollector
            dataCollector.collect(averagedMetrics, payloadId, serializationFormat);

        } catch (IOException e) {
            System.err.println("Erro na pipeline: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void accumulate(Map<String, ServiceMetricsAccumulator> map, ServiceMetrics m) {
        if (m == null) return;
        map.computeIfAbsent(m.getServiceName(), k -> new ServiceMetricsAccumulator(m.getServiceName()))
           .add(m);
    }

    // Classe interna para ajudar no cálculo da média
    private static class ServiceMetricsAccumulator {
        private final String serviceName;
        private long totalDeTime = 0;
        private long totalSeTime = 0;
        private long totalTime = 0;
        private long totalRAM = 0;
        private long messageSize = 0; 

        public ServiceMetricsAccumulator(String serviceName) {
            this.serviceName = serviceName;
        }

        public void add(ServiceMetrics m) {
            this.totalDeTime += m.getDeserializationTimeMs();
            this.totalSeTime += m.getSerializationTimeMs();
            this.totalTime += m.getTotalProcessingTimeMs();
            this.totalRAM += m.getMemoryUsedBytes();
            this.messageSize = m.getMessageSizeBytes();
        }
    }
}
