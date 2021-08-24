-- Cada execução tem um id em dataflow e seu timestamp em dataflow_execution: consulta de tempos de execução para cada execução realizada.
-- todas as execucoes foram executadas em sequencia ou houve paralelismo na execucao ? pq oq estou fazendo pra definir tempo de execucao eh pegar a hr de inicio da execucao seguinte e reduzir da hr de inicio da execucao atual
select
	t.id,
	t.next_execution_datetime,
	t.execution_datetime,
	COALESCE(t.next_execution_datetime,t.execution_datetime) - t.execution_datetime as execution_time
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
	execution_time,t.id;
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