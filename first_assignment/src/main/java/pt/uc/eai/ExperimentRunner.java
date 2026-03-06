package pt.uc.eai;

import com.fasterxml.jackson.databind.ObjectMapper;
import pt.uc.eai.Forma.SerializationFormat;
import pt.uc.eai.generator.PayloadGenerator;
import pt.uc.eai.model.Payload;
import pt.uc.eai.pipeline.PipelineRunner;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ExperimentRunner {

    public void run() {
        // Load all parameters from config.properties
        long seed = Config.getLongProperty("generator.seed", 42L);
        String streamId = Config.getProperty("generator.streamId", "stream_default");
        int audioLen = Config.getIntProperty("generator.audioLen", 10);
        int pixelsLen = Config.getIntProperty("generator.pixelsLen", 10);
        int metadataLen = Config.getIntProperty("generator.metadataLen", 10);

        int framesPerChunk = Config.getIntProperty("experiment.framesPerChunk", 100);

        int[] chunkSizes = parseIntArray(Config.getProperty("experiment.chunkSizes", "10,20,50,100,200,500,1000"));
        SerializationFormat[] formats = parseFormats(Config.getProperty("experiment.formats", "JSON,BSON"));

        System.out.println("=== Experiment Runner ===");
        System.out.println("Formats     : " + Arrays.toString(formats));
        System.out.println("Chunk sizes : " + Arrays.toString(chunkSizes));
        System.out.println("FPC (fixed) : " + framesPerChunk);
        System.out.println("Iterations  : " + Config.getProperty("pipeline.iterations", "30"));
        System.out.println("========================\n");

        for (SerializationFormat format : formats) {
            for (int numChunks : chunkSizes) {
                ExperimentConfig expConfig = new ExperimentConfig(format, numChunks, framesPerChunk);
                System.out.printf("%n[EXPERIMENT] %s%n", expConfig);

                ObjectMapper mapper = Forma.createMapper(format);
                PayloadGenerator gen = new PayloadGenerator(seed);
                Payload payload = gen.generate(streamId, numChunks, framesPerChunk, audioLen, pixelsLen, metadataLen);

                PipelineRunner runner = new PipelineRunner(mapper);
                runner.runExperiment(payload, expConfig);
            }
        }

        System.out.println("\n=== All experiments completed. Results saved to stats.csv ===");
    }

    private static int[] parseIntArray(String csv) {
        String[] parts = csv.split(",");
        int[] result = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            result[i] = Integer.parseInt(parts[i].trim());
        }
        return result;
    }

    private static SerializationFormat[] parseFormats(String csv) {
        String[] parts = csv.split(",");
        List<SerializationFormat> result = new ArrayList<>();
        for (String part : parts) {
            result.add(SerializationFormat.valueOf(part.trim().toUpperCase()));
        }
        return result.toArray(new SerializationFormat[0]);
    }
}
