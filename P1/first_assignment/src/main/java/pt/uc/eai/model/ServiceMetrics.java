package pt.uc.eai.model;

public class ServiceMetrics {
    private final String serviceName;
    private final long deserializationTimeMs;
    private final long serializationTimeMs;
    private final long totalProcessingTimeMs;
    private final long messageSizeBytes;
    private final long memoryUsedBytes;

    public ServiceMetrics(String serviceName, long deserializationTimeMs, long serializationTimeMs, 
                          long totalProcessingTimeMs, long messageSizeBytes, long memoryUsedBytes) {
        this.serviceName = serviceName;
        this.deserializationTimeMs = deserializationTimeMs;
        this.serializationTimeMs = serializationTimeMs;
        this.totalProcessingTimeMs = totalProcessingTimeMs;
        this.messageSizeBytes = messageSizeBytes;
        this.memoryUsedBytes = memoryUsedBytes;
    }

    public String getServiceName() { return serviceName; }
    public long getDeserializationTimeMs() { return deserializationTimeMs; }
    public long getSerializationTimeMs() { return serializationTimeMs; }
    public long getTotalProcessingTimeMs() { return totalProcessingTimeMs; }
    public long getMessageSizeBytes() { return messageSizeBytes; }
    public long getMemoryUsedBytes() { return memoryUsedBytes; }

    @Override
    public String toString() {
        return String.format("%s, %dms (de), %dms (se), %dms (total), %d bytes, %d bytes (RAM)",
                serviceName, deserializationTimeMs, serializationTimeMs, totalProcessingTimeMs, messageSizeBytes, memoryUsedBytes);
    }
}
