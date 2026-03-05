package pt.uc.eai;

import com.fasterxml.jackson.databind.ObjectMapper;

import pt.uc.eai.generator.PayloadGenerator;
import pt.uc.eai.model.Payload;

public class Main {
    public static void main(String[] args) {
        
        // Configurações do gerador
        long seed = Config.getLongProperty("generator.seed", 42L);
        String streamId = Config.getProperty("generator.streamId", "stream_default");
        int numChunks = Config.getIntProperty("generator.numChunks", 2);
        int framesPerChunk = Config.getIntProperty("generator.framesPerChunk", 3);
        int audioLen = Config.getIntProperty("generator.audioLen", 5);
        int pixelsLen = Config.getIntProperty("generator.pixelsLen", 10);
        int metadataLen = Config.getIntProperty("generator.metadataLen", 3);

        // Configuração do formato de serialização
        Forma.SerializationFormat format = Forma.getFormatFromConfig();
        ObjectMapper mapper = Forma.createMapper(format);
        
        System.out.println("\n[CONFIGURAÇÃO] Formato de serialização: " + format);

        PayloadGenerator gen = new PayloadGenerator(seed);

        Payload payload = gen.generate(
                streamId,
                numChunks,
                framesPerChunk,
                audioLen,
                pixelsLen,
                metadataLen
        );

        System.out.println("[SISTEMA] Payload gerado com sucesso.");
        System.out.println("- Stream ID: " + payload.getStreamId());
        int totalFrames = numChunks * framesPerChunk;
        System.out.println("- Total de Frames: " + totalFrames);

        pt.uc.eai.pipeline.PipelineRunner pipeline = new pt.uc.eai.pipeline.PipelineRunner(mapper);
        pipeline.run(payload);
    }
}
