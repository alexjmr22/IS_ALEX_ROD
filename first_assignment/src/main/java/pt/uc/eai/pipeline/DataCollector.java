package pt.uc.eai.pipeline;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

import pt.uc.eai.model.ServiceMetrics;

public class DataCollector {

    public DataCollector(com.fasterxml.jackson.databind.ObjectMapper mapper) {
        // mapper não é usado diretamente aqui agora, mas mantido por compatibilidade
    }

    public void collect(List<ServiceMetrics> metricsList, String format, int numChunks, int framesPerChunk) throws IOException {
        System.out.printf("[DataCollector] Gravando métricas: format=%s, numChunks=%d, framesPerChunk=%d%n",
                format, numChunks, framesPerChunk);

        File statsFile = new File("stats.csv");
        boolean isNew = !statsFile.exists();

        try (FileWriter fw = new FileWriter(statsFile, true);
             PrintWriter out = new PrintWriter(fw)) {

            // Header apenas se o ficheiro for novo
            if (isNew) {
                out.println("format,numChunks,framesPerChunk,service,serialization_ms,deserialization_ms,total_ms,message_size_bytes,ram_bytes,timestamp");
            }

            for (ServiceMetrics m : metricsList) {
                out.printf("%s,%d,%d,%s,%d,%d,%d,%d,%d,%d%n",
                        format,
                        numChunks,
                        framesPerChunk,
                        m.getServiceName(),
                        m.getSerializationTimeMs(),
                        m.getDeserializationTimeMs(),
                        m.getTotalProcessingTimeMs(),
                        m.getMessageSizeBytes(),
                        m.getMemoryUsedBytes(),
                        System.currentTimeMillis());

                System.out.println(" - " + m.toString());
            }
        }

        System.out.println("[DataCollector] Ficheiro " + statsFile.getAbsolutePath() + " guardado com sucesso.");
    }
}
