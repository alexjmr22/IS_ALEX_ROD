package pt.uc.eai;

import pt.uc.eai.generator.PayloadGenerator;
import pt.uc.eai.model.Payload;
// Bibliotecas do Jackson para lidar com JSON (Serialização/Deserialização)
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class Main {
    public static void main(String[] args) {
        long seed = Config.getLongProperty("generator.seed", 42L);
        String streamId = Config.getProperty("generator.streamId", "stream_default");
        int numChunks = Config.getIntProperty("generator.numChunks", 2);
        int framesPerChunk = Config.getIntProperty("generator.framesPerChunk", 3);
        int audioLen = Config.getIntProperty("generator.audioLen", 5);
        int pixelsLen = Config.getIntProperty("generator.pixelsLen", 10);
        int metadataLen = Config.getIntProperty("generator.metadataLen", 3);
        String nameFile = Config.getProperty("generator.nameFile", "payload.json");
        PayloadGenerator gen = new PayloadGenerator(seed);

        Payload payload = gen.generate(
                streamId,
                numChunks,
                framesPerChunk,
                audioLen,
                pixelsLen,
                metadataLen
        );

        System.out.println("\n[SISTEMA] Payload gerado com sucesso.");
        System.out.println("- Stream ID: " + payload.getStreamId());
        int totalFrames = numChunks * framesPerChunk;
        System.out.println("- Total de Frames: " + totalFrames);
        
        // Exportação automática para JSON
        exportToJson(payload, nameFile, totalFrames);
    }

    /**
     * Serializa o objeto Payload para um ficheiro JSON usando Jackson.
     * Útil para comparar o tamanho final e desempenho de serialização.
     */
    private static void exportToJson(Payload payload, String nameFile, int totalFrames) {
        try {
            // ObjectMapper é o motor que converte objetos Java em JSON
            ObjectMapper mapper = new ObjectMapper();
            
            // Ativa a indentação para o JSON ser mais fácil de ler para humanos
            mapper.enable(SerializationFeature.INDENT_OUTPUT);
            
            File outputFile = new File(nameFile);

            // Começar a cronometrar a operação de serialização
            long startTime = System.nanoTime();
            
            // Escrita efetiva no ficheiro
            mapper.writeValue(outputFile, payload);
            
            long endTime = System.nanoTime();
            long durationMs = (endTime - startTime) / 1000000;
            long fileSizeKb = outputFile.length() / 1024;

            System.out.println("\n[SISTEMA] Payload exportado com sucesso!");
            System.out.println("- Local: " + outputFile.getAbsolutePath());
            System.out.println("- Tempo de Serialização: " + durationMs + " ms");
            System.out.println("- Tamanho do Ficheiro: " + fileSizeKb + " KB");

            // Escrever estatísticas num ficheiro CSV (append mode)
            saveStats(nameFile, durationMs, fileSizeKb, totalFrames);

        } catch (IOException e) {
            System.err.println("[ERRO] Falha ao exportar para JSON: " + e.getMessage());
        }
    }

    /**
     * Guarda as estatísticas de execução num ficheiro CSV.
     * Inclui o nome do utilizador para distinguir testes entre membros do grupo.
     */
    private static void saveStats(String nameFile, long durationMs, long fileSizeKb, int totalFrames) {
        File statsFile = new File("stats.csv");
        boolean isNew = !statsFile.exists();
        String user = System.getProperty("user.name", "unknown");

        try (FileWriter fw = new FileWriter(statsFile, true);
             PrintWriter out = new PrintWriter(fw)) {
            
            if (isNew) {
                out.println("User,File,TotalFrames,TimeMs,SizeKB,Timestamp");
            }

            out.printf("%s,%s,%d,%d,%d,%d%n", 
                       user, nameFile, totalFrames, durationMs, fileSizeKb, System.currentTimeMillis());
                       
        } catch (IOException e) {
            System.err.println("[ERRO] Falha ao guardar estatísticas: " + e.getMessage());
        }
    }
}
