package pt.uc.eai.pipeline;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

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
        try {
            System.out.println("Iniciando Pipeline com Métricas: Encoder -> AudioService -> VideoService -> MetadataService -> DataCollector");

            // 1. Encoder
            byte[] originalPacket = encoder.encode(initialPayload);
            
            // 2. AudioService
            audioService.process(originalPacket);
            
            // 3. VideoService
            videoService.process(originalPacket);
            
            // 4. MetadataService
            metadataService.process(originalPacket);

            // Coletar métricas
            List<ServiceMetrics> allMetrics = new ArrayList<>();
            allMetrics.add(audioService.getMetrics());
            allMetrics.add(videoService.getMetrics());
            allMetrics.add(metadataService.getMetrics());

            // Identificador baseado no nome do ficheiro ou configuração ativa
            String payloadId = Config.getProperty("generator.nameFile", "unknown_payload");

            // 5. DataCollector
            dataCollector.collect(allMetrics, payloadId, serializationFormat);

        } catch (IOException e) {
            System.err.println("Erro na pipeline: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
