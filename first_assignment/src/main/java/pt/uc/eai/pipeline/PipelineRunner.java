package pt.uc.eai.pipeline;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.databind.ObjectMapper;

import pt.uc.eai.Config;
import pt.uc.eai.ExperimentConfig;
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

    public PipelineRunner(ObjectMapper mapper) {
        this.encoder = new Encoder(mapper);
        this.audioService = new AudioService(mapper);
        this.videoService = new VideoService(mapper);
        this.metadataService = new MetadataService(mapper);
        this.dataCollector = new DataCollector(mapper);
    }

    public void runExperiment(Payload initialPayload, ExperimentConfig expConfig) {
        int iterations = Integer.parseInt(Config.getProperty("pipeline.iterations", "1"));
        System.out.printf("Pipeline: %d iterations | %s%n", iterations, expConfig);

        List<ServiceMetrics> allMetrics = new ArrayList<>();

        try {
            for (int i = 0; i < iterations; i++) {
                if (iterations > 1) {
                    System.out.println("  Iteração " + (i + 1) + "/" + iterations + "...");
                }

                // 1. Encoder
                byte[] originalPacket = encoder.encode(initialPayload);

                // 2. AudioService
                audioService.process(originalPacket);

                // 3. VideoService
                videoService.process(originalPacket);

                // 4. MetadataService
                metadataService.process(originalPacket);

                if (audioService.getMetrics() != null) allMetrics.add(audioService.getMetrics());
                if (videoService.getMetrics() != null) allMetrics.add(videoService.getMetrics());
                if (metadataService.getMetrics() != null) allMetrics.add(metadataService.getMetrics());
            }

            // 5. DataCollector
            dataCollector.collect(allMetrics, expConfig.getFormat().name(),
                    expConfig.getNumChunks(), expConfig.getFramesPerChunk());

        } catch (IOException e) {
            System.err.println("Erro na pipeline: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
