import argparse
import multiprocessing
import sys
import uvicorn

def run_api():
    """Arranca o servidor FastAPI"""
    print("A iniciar o servidor FastAPI na porta 8001...")
    # Importar em tempo de execução para evitar potenciais problemas circulares
    # Usamos o caminho da string para que o uvicorn possa recarregar (reload=True)
    uvicorn.run("football:app", host="127.0.0.1", port=8001, reload=False)

def run_mcp():
    """Arranca o servidor FastMCP"""
    print("A iniciar o servidor FastMCP na porta 8002...")
    from mcp_server import mcp
    mcp.run(transport="sse", host="127.0.0.1", port=8002)

def main():
    parser = argparse.ArgumentParser(description="Ponto de entrada para a aplicação de Futebol")
    parser.add_argument(
        "servico", 
        choices=["api", "mcp", "ambos"], 
        nargs="?", 
        default="ambos",
        help="Serviço a arrancar: 'api' (FastAPI), 'mcp' (FastMCP) ou 'ambos' (por defeito)"
    )
    
    args = parser.parse_args()
    
    if args.servico == "api":
        run_api()
    elif args.servico == "mcp":
        run_mcp()
    elif args.servico == "ambos":
        print("====== A INICIAR AMBOS OS SERVIÇOS ======")
        p_api = multiprocessing.Process(target=run_api)
        p_mcp = multiprocessing.Process(target=run_mcp)
        
        p_api.start()
        p_mcp.start()
        
        try:
            # Mantém o processo principal vivo para poder escutar o CTRL+C
            p_api.join()
            p_mcp.join()
        except KeyboardInterrupt:
            print("\n!!! A encerrar ambos os serviços !!!")
            p_api.terminate()
            p_mcp.terminate()
            p_api.join()
            p_mcp.join()
            sys.exit(0)

if __name__ == "__main__":
    main()
