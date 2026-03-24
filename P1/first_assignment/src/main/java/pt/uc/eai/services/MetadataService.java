package pt.uc.eai.services;

import pt.uc.eai.model.Payload;
import pt.uc.eai.model.Chunk;
import pt.uc.eai.model.Frame;
import pt.uc.eai.model.ServiceMetrics;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;

public class MetadataService {
    private final ObjectMapper mapper;
    private ServiceMetrics metrics;

    public MetadataService(ObjectMapper mapper) {
        this.mapper = mapper;
    }

    public byte[] process(byte[] packet) throws IOException {
        System.gc();
        long startTime = System.nanoTime();
        long startMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        long startDe = System.nanoTime();
        Payload payload = mapper.readValue(packet, Payload.class);
        long endDe = System.nanoTime();

        for (Chunk chunk : payload.getChunks()) {
            for (Frame frame : chunk.getFrames()) {
                for (Double meta : frame.getMetadata()) {
                   double v = meta;
                }
            }
        }

        long startSe = System.nanoTime();
        byte[] result = mapper.writeValueAsBytes(payload);
        long endSe = System.nanoTime();

        long endMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        long endTime = System.nanoTime();

        long memUsed = endMem - startMem;
        if (memUsed <= 0) memUsed = result.length;

        this.metrics = new ServiceMetrics(
            "MetadataService", (endDe - startDe) / 1000000, (endSe - startSe) / 1000000,
            (endTime - startTime) / 1000000, result.length, memUsed
        );
        return result;
    }

    public ServiceMetrics getMetrics() { return metrics; }
}
