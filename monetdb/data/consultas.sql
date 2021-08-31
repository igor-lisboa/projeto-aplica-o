
-- Cada execução tem um id em dataflow e seu timestamp em dataflow_execution: consulta de tempos de execução para cada execução realizada.
-- todas as execucoes foram executadas em sequencia ou houve paralelismo na execucao ? pq oq estou fazendo pra definir tempo de execucao eh pegar a hr de inicio da execucao seguinte e reduzir da hr de inicio da execucao atual
select
	t.id,
	t.next_execution_datetime,
	t.execution_datetime,
	coalesce(t.next_execution_datetime,
	t.execution_datetime) - t.execution_datetime as execution_time
from
	(
	select
		d.id,
		LEAD( sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over (
	order by
		de.execution_datetime,
		d.id) as next_execution_datetime,
		sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime
	from
		dataflow d
	left join dataflow_execution de on
		(d.id = de.df_id)
	order by
		de.execution_datetime,
		d.id) t
order by
	execution_time,
	t.id;
-- Cada data transformation tem um id de execução em data_transformation_execution e o momento que começou a executar (timestamp): consulta de duração de execução por transformação.
select
	t.data_transformation_id,
	t.data_transformation_tag,
	sum(coalesce(t.next_execution_datetime,
	t.current_execution_datetime) - t.current_execution_datetime) as execution_time
from
	(
	select
		dte.id,
		dte.dataflow_execution_id,
		dte.data_transformation_id,
		dt.tag as data_transformation_tag,
		sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') as current_execution_datetime,
		LEAD( sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over (
	order by
		dte.execution_datetime,
		dte.id) as next_execution_datetime
	from
		data_transformation_execution dte
	left join data_transformation dt on
		(dt.id = dte.data_transformation_id)
		) t
group by
	t.data_transformation_id,
	t.data_transformation_tag;
-- 	A telemetria foi capturada em intervalos de 20/30s (uso de cpu, disco, memória). Em  telemetry tem o id de execução de cada transformação executada (data_transformation_execution_id): Consulta para identificar consumo de recurso por transformação (relacionando telemetry data_transformation_execution_id com data_transformation) e por dataflow.
select
	t.data_transformation_execution_id,
	dt.tag,
	count(t.data_transformation_execution_id) as count_data_transformation_exec,
	avg(tm.svmem_total) as avg_svmem_total,
	sum(tm.svmem_total) as sum_svmem_total,
	avg(tm.svmem_available) as avg_svmem_available,
	sum(tm.svmem_available) as sum_svmem_available,
	avg(tm.svmem_used) as avg_svmem_used,
	sum(tm.svmem_used) as sum_svmem_used,
	avg(cast( tc.scputimes_user as double)) as avg_scputimes_user,
	sum(cast( tc.scputimes_user as double)) as sum_scputimes_user,
	avg(cast( tc.scputimes_system as double)) as avg_scputimes_system,
	sum(cast( tc.scputimes_system as double)) as sum_scputimes_system,
	avg(cast( tc.scputimes_idle as double)) as avg_scputimes_idle,
	sum(cast( tc.scputimes_idle as double)) as sum_scputimes_idle,
	avg(cast( tc.scputimes_steal as double)) as avg_scputimes_steal,
	sum(cast( tc.scputimes_steal as double)) as sum_scputimes_steal,
	avg(cast( td.sdiskio_read_bytes as double)) as avg_sdiskio_read_bytes,
	sum(cast( td.sdiskio_read_bytes as double)) as sum_sdiskio_read_bytes,
	avg(cast( td.sdiskio_write_bytes as double)) as avg_sdiskio_write_bytes,
	sum(cast( td.sdiskio_write_bytes as double)) as sum_sdiskio_write_bytes,
	avg(cast( td.sdiskio_busy_time as double)) as avg_sdiskio_busy_time,
	sum(cast( td.sdiskio_busy_time as double)) as sum_sdiskio_busy_time,
	avg(cast( td.sswap_total as double)) as avg_sswap_total,
	sum(cast( td.sswap_total as double)) as sum_sswap_total
	--avg(cast( td.sswap_used as double)) as avg_sswap_used, => nao usado pq os valores estao com a string 'null'
	--sum(cast( td.sswap_used as double)) as sum_sswap_used => nao usado pq os valores estao com a string 'null'
from
	data_transformation dt
left join telemetry t on
	(t.data_transformation_execution_id = dt.id)
left join dataflow d on
	(dt.df_id = d.id)
left join telemetry_cpu tc on
	(t.id = tc.telemetry_id)
left join telemetry_disk td on
	(t.id = td.telemetry_id )
left join telemetry_memory tm on
	(t.id = tm.telemetry_id)
where
	t.data_transformation_execution_id is not null
group by
	t.data_transformation_execution_id,
	dt.tag
order by
	2 desc;
--Consulta de domínio: quantitativo de modelos evolutivos calculados -> disponíveis nos datasets de  saída da transformação modelgeneratormodule_raxml ou _mrb (ds_omodelgeneratormodule_mrb, _raxml)
