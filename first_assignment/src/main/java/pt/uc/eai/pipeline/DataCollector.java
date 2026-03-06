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

    public void collect(List<ServiceMetrics> metricsList, String payloadId, String format) throws IOException {
        System.out.println("[DataCollector] Gravando métricas de desempenho para: " + payloadId + " (formato: " + format + ")");

        File statsFile = new File("stats.csv");
        boolean isNew = !statsFile.exists();

        try (FileWriter fw = new FileWriter(statsFile, true);
             PrintWriter out = new PrintWriter(fw)) {
            
            // Header apenas se o ficheiro for novo
            if (isNew) {
                out.println("PayloadID,Format,Service,AvgDeTimeMs,AvgSeTimeMs,AvgTotalTimeMs,Size_Bytes,AvgRAM_Bytes,Timestamp");
            }

            for (ServiceMetrics m : metricsList) {
                out.printf("%s,%s,%s,%d,%d,%d,%d,%d,%d%n", 
                           payloadId,
                           format,
                           m.getServiceName(), 
                           m.getDeserializationTimeMs(), 
                           m.getSerializationTimeMs(), 
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
