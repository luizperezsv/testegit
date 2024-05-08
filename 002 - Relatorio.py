import pandas as pd
import fdb

# Conectar ao banco de dados Firebird
conn = fdb.connect(
    host="10.171.0.31", 
    database="siap2023",
    user="sysdba", 
    password="wildfire"
)

# Escreva sua consulta SQL
sql_query = """
 SELECT
ld.d020 tributo,
t.descricao,
count(*) quantidade,
sum(ld.d010) total,
ao.processo,
cast(ao.historico as varchar(1000)) historico,
tc.ds_ocorrencia motivo,
cast(udf_trim(ld.d017)||'/'||ld.d028 as char(20)) as cda


FROM
geda_ldivida ld
left join aac_ocorrencias ao on ao.ref_origem = ld.d000
left join tri_tributos t on t.tributo = ld.d020
left join tri_ocorrencia tc on tc.id_ocorrencia = ao.id_ocorrencia
WHERE
ld.d029 in (4) -- em aberto ou em acordo
and ld.d016 IN ('N','p') -- nao ajuizado
and ao.tipo in ('GECD','GEPR')
and (ao.historico like '%ancel%' or
ao.historico like '%tinç%')
AND AO.data BETWEEN '01.01.2023' AND '31.12.2023'
GROUP BY 1,2,5,6,7,8
"""

# Use o pandas para ler os resultados da consulta SQL em um DataFrame
df = pd.read_sql(sql_query, conn)

# Salve o DataFrame em um arquivo do Excel
df.to_excel('C:/Users/luizperez/Documents/Demandas Kelly/Paulo/versao 5/resultado_da_consulta.xlsx', index=False)

# Feche a conexão com o banco de dados
conn.close()

print("Consulta salva com sucesso no Excel!")
