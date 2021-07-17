create function insertuser (vname varchar(50), vemail varchar(50))
returns integer
begin
 declare vid integer;
 select id into vid from user_table where name=vname and email=vemail;
 if(vid is null) then
 select next value for "user_id_seq" into vid;
 insert into user_table(id,name,email) values (vid,vname,vemail);
 end if;
 return vid;
end;
create function insertphysicalmachine (vname varchar(50), vip varchar(50), vmac varchar(50), vowner_user_id integer, vram integer, vdisk integer)
returns integer
begin
 declare vid integer;
 select id into vid from physical_machine where name=vname and ip=vip;
 if(vid is null) then
 select next value for "physical_machine_id_seq" into vid;
 insert into physical_machine(id,name,ip,mac,owner_user_id,ram,disk) values (vid,vname,vip,vmac,vowner_user_id,vram,vdisk);
 end if;
 return vid;
end;
create function insertvirtualmachine (vname varchar(50), vram integer, vdisk integer, vphysical_machine_id integer)
returns integer
begin
 declare vid integer;
 select id into vid from virtual_machine where name=vname and physical_machine_id=vphysical_machine_id;
 if(vid is null) then
 select next value for "virtual_machine_id_seq" into vid;
 insert into virtual_machine(id,name,ram,disk,physical_machine_id) values (vid,vname,vram,vdisk,vphysical_machine_id);
 end if;
 return vid;
end;
create function insertdataflow (v_tag varchar(50), vuser_id integer)
returns integer
begin
 declare v_df_id integer;
 select df.id into v_df_id from dataflow df where df.tag=v_tag and df.user_id=vuser_id;
 if(v_df_id is null) then
 select next value for "df_id_seq" into v_df_id;
 insert into dataflow(id,tag,user_id) values (v_df_id,v_tag,vuser_id);
 end if;
 return v_df_id;
end;
create function insertprogram (vdt_id integer, vname varchar(200), vversion varchar(50))
returns integer
begin
 declare vprogram_id integer;
 select id into vprogram_id from program p where name = vname and version = vversion;
 if(vprogram_id is null) then
 select next value for "program_id_seq" into vprogram_id;
 insert into program(id,name,version) values (vprogram_id,vname,vversion);
 end if;
 return vprogram_id;
end;
create function insertdatatransformation (vtag varchar(50), vdf_id integer, vprogram_id integer)
returns integer
begin
 declare vid integer;
 select id into vid from data_transformation where df_id = vdf_id and tag = vtag;
 if(vid is null) then
 select next value for "dt_id_seq" into vid;
 insert into data_transformation(id,tag,df_id,program_id) values (vid,vtag,vdf_id,vprogram_id);
 end if;
 return vid;
end;
create function insertdataflowversion (vdf_id integer)
returns integer
begin
 declare version_id integer;
 select next value for "version_id_seq" into version_id;
 insert into dataflow_version(version,df_id) values (version_id,vdf_id);
 return version_id;
end;
create function insertdataset (vdf_id integer, vdt_id integer, vdep_dt_id integer, vtag varchar(5000), vtype varchar(10))
returns integer
begin
 declare vds_id integer;
 select id into vds_id from data_set ds where df_id = vdf_id and tag = vtag;
 if(vds_id is null) then
 select next value for "ds_id_seq" into vds_id;
 insert into data_set(id,df_id,tag) values (vds_id,vdf_id,vtag);
 end if;
 if(vdep_dt_id is not null) then
 declare vdd_id integer;
 select ds_id into vdd_id from data_dependency
 where previous_dt_id = vdep_dt_id and next_dt_id = vdt_id and ds_id = vds_id;
 declare vid integer;
 select id into vid from data_dependency where previous_dt_id = vdep_dt_id and next_dt_id is null;
 if(vid is null) then
 if(vdd_id is null) then
 declare vdd_id integer;
 select next value for "dd_id_seq" into vdd_id;
 insert into data_dependency(id,previous_dt_id,next_dt_id,ds_id) values (vdd_id,vdep_dt_id,vdt_id,vds_id);
 end if;
 else
 update data_dependency set next_dt_id = vdt_id where id = vid;
 end if;
 else
 declare vdd_id integer;
 select next value for "dd_id_seq" into vdd_id;
 if(vtype like 'INPUT') then
 insert into data_dependency(id,previous_dt_id,next_dt_id,ds_id) values (vdd_id,null,vdt_id,vds_id);
 else
 insert into data_dependency(id,previous_dt_id,next_dt_id,ds_id) values (vdd_id,vdt_id,null,vds_id);
 end if;
 end if;
 return vds_id;
end;
create function insertattribute (dds_id integer, vextractor_id integer, vname varchar(30), vtype varchar(15))
returns integer
begin
 declare vid integer;
 select id into vid from attribute where ds_id=dds_id and name=vname;
 if(vid is null) then
 select next value for "att_id_seq" into vid;
 insert into attribute(id,ds_id,extractor_id,name,type) values (vid,dds_id,vextractor_id,vname,vtype);
 end if;
 return vid;
end;
create function inserttask (videntifier integer, vdf_tag varchar(50), vdt_tag varchar(50), vstatus varchar(10), vworkspace varchar(5000), 
 vcomputing_resource varchar(100), voutput_msg text, verror_msg text)
returns integer
begin
 declare vid integer;
 declare vvstatus varchar(10);
 declare vdf_version integer;
 declare vdt_id integer;
 select dfv.version, dt.id into vdf_version, vdt_id
 from dataflow df, data_transformation dt, dataflow_version as dfv
 where df.id = dt.df_id and dfv.df_id = df.id and df.tag = vdf_tag and dt.tag = vdt_tag;
 if((vdf_version is not null) and (vdt_id is not null)) then
 select t.id, t.status into vid, vvstatus
 from task t
 where t.df_version = vdf_version and t.dt_id = vdt_id and t.identifier = videntifier;
 if(vid is null) then
 select next value for "task_id_seq" into vid;
 insert into task(id,identifier,df_version,dt_id,status,workspace,computing_resource,output_msg,error_msg) 
 values (vid,videntifier,vdf_version,vdt_id,vstatus,vworkspace,vcomputing_resource,voutput_msg,verror_msg);
 else
 update task
 set status = vstatus, output_msg = voutput_msg, error_msg = verror_msg
 where identifier = videntifier and df_version = vdf_version and dt_id = vdt_id;
 end if;
 end if;
 return vid;
end;
create function insertfile (vname varchar(200), vpath varchar(5000), vid_file_type integer)
returns integer
begin
 declare vid integer;
 select id into vid from file where name=vname and path=vpath;
 if(vid is null) then
 select next value for "file_id_seq" into vid;
 insert into file(id,name,path,id_file_type) values (vid,vname,vpath,vid_file_type);
 end if;
 return vid;
end;
create function insertfiletype (vname varchar(200))
returns integer
begin
 declare vid integer;
 select id into vid from file_type where name=vname;
 if(vid is null) then
 select next value for "file_type_id_seq" into vid;
 insert into file_type(id, name) values (vid, vname);
 end if;
 return vid;
end;
create function insertperformance (vtask_id integer, vsubtask_id integer, vmethod varchar(30), vdescription varchar(200), vstarttime varchar(30), vendtime varchar(30), vinvocation text)
returns integer
begin
 declare vid integer;
 if(vsubtask_id is null) then
 select id into vid from performance where method=vmethod and task_id=vtask_id;
 else
 select id into vid from performance where method=vmethod and task_id=vtask_id and subtask_id=vsubtask_id;
 end if;
 
 if(vid is null) then
 select next value for "performance_id_seq" into vid;
 insert into performance(id,task_id,subtask_id,method,description,starttime,endtime,invocation) values (vid,vtask_id,vsubtask_id,vmethod,vdescription,vstarttime,vendtime,vinvocation);
 else
 update performance
 set endtime = vendtime, invocation = vinvocation
 where id = vid and endtime = 'null';
 end if;
 return vid;
end;
create function insertextractor (vtag varchar(20), vds_id integer, vcartridge varchar(20), vextension varchar(20))
returns integer
begin
 declare vid integer;
 select id into vid from extractor where tag = vtag and ds_id = vds_id and cartridge = vcartridge and extension = vextension;
 if(vid is null) then
 select next value for "extractor_id_seq" into vid;
 insert into extractor(id,ds_id,tag,cartridge,extension) values (vid,vds_id,vtag,vcartridge,vextension);
 end if;
 return vid;
end;
create function insertextractorcombination (vouter_ext_id integer, vinner_ext_id integer, vds_id integer, vkeys varchar(100), vkey_types varchar(100))
returns integer
begin
 declare vid integer;
 select id into vid from extractor_combination where outer_ext_id = vouter_ext_id and inner_ext_id = vinner_ext_id and ds_id = vds_id;
 if(vid is null) then
 select next value for "ecombination_id_seq" into vid;
 insert into extractor_combination(outer_ext_id,inner_ext_id,keys,key_types,ds_id) values (vouter_ext_id,vinner_ext_id,vkeys,vkey_types,vds_id);
 end if;
 return vid;
end;
create function insertepoch (vvalue integer, velapsed_time decimal(10,2), vloss decimal(10,2), vaccuracy decimal(10,2), vepoch_timestamp varchar(30), vtask_id integer, vdata_transformation_execution_id integer)
returns integer
begin
 declare vid integer;
 select id into vid from epoch where value=vvalue and task_id =vtask_id;
 if(vid is null) then
 select next value for "epoch_id_seq" into vid;
 insert into epoch(id,value,elapsed_time,loss, accuracy, epoch_timestamp, task_id, data_transformation_execution_id) values (vid,vvalue, velapsed_time, vloss, vaccuracy, vepoch_timestamp, vtask_id, vdata_transformation_execution_id);
 end if;
 return vid;
end;
create function insertdataflowexecution (vexecution_datetime varchar(30), vdf_id integer, vphysical_machine_id integer, vvirtual_machine_id integer)
returns integer
begin
 declare vid integer;
 select id into vid from dataflow_execution where execution_datetime=vexecution_datetime and df_id=vdf_id and physical_machine_id=vphysical_machine_id and virtual_machine_id=vvirtual_machine_id;
 if(vid is null) then
 select next value for "df_exec_id_seq" into vid;
 insert into dataflow_execution(id,execution_datetime,df_id,physical_machine_id,virtual_machine_id) values (vid,vexecution_datetime,vdf_id,vphysical_machine_id,vvirtual_machine_id);
 end if;
 return vid;
end;
create function insertdatatransformationexecution (vdataflow_execution_id integer, vdata_transformation_tag varchar(50), vexecution_datetime varchar(30))
returns integer
begin
 declare vid integer;
 declare vdt_id integer;
 select dt.id into vdt_id
 from dataflow_execution dfe, data_transformation dt
 where dfe.df_id = dt.df_id and dt.tag = vdata_transformation_tag and dfe.id = vdataflow_execution_id;
 if(vdt_id is not null) then
 select id into vid from data_transformation_execution where dataflow_execution_id=vdataflow_execution_id and data_transformation_id=vdt_id and execution_datetime=vexecution_datetime;
 if(vid is null) then
 select next value for "dt_exec_id_seq" into vid;
 insert into data_transformation_execution(id,dataflow_execution_id,data_transformation_id,execution_datetime) values (vid,vdataflow_execution_id,vdt_id,vexecution_datetime);
 end if;
 end if;
 return vid;
end;
create function insertfiletransformationexecution (vfile_id integer, vgeneration_datetime varchar(30), vlast_modification_datetime varchar(30), vdata_transformation_execution_id integer)
returns integer
begin
 declare vid integer;
 select id into vid from file_transformation_execution where file_id=vfile_id and generation_datetime=vgeneration_datetime;
 if(vid is null) then
 select next value for "file_dt_id_seq" into vid;
 insert into file_transformation_execution(id,file_id,generation_datetime,last_modification_datetime,data_transformation_execution_id) values (vid,vfile_id,vgeneration_datetime,vlast_modification_datetime,vdata_transformation_execution_id);
 end if;
 return vid;
end;
create function inserttelemetry (vtask_id integer, vcaptured_timestamp varchar(30), vcaptured_interval varchar(30), vdata_transformation_execution_id integer)
returns integer
begin
 declare vid integer;
 select id into vid from telemetry where captured_timestamp=vcaptured_timestamp and task_id =vtask_id;
 if(vid is null) then
 select next value for "telemetry_id_seq" into vid;
 insert into telemetry(id, task_id, captured_timestamp, captured_interval, data_transformation_execution_id) values (vid, vtask_id, vcaptured_timestamp, vcaptured_interval, vdata_transformation_execution_id);
 end if;
 return vid;
end;
create function inserttelemetrycpu (vtelemetry_id integer, vconsumption_timestamp varchar(30), vscputimes_user varchar(30), vscputimes_system varchar(30), vscputimes_idle varchar(30), vscputimes_steal varchar(30))
returns integer
begin
 declare vid integer;
 select id into vid from telemetry_cpu where consumption_timestamp=vconsumption_timestamp ;
 if(vid is null) then
 select next value for "telemetry_cpu_id_seq" into vid;
 insert into telemetry_cpu(id, telemetry_id, consumption_timestamp, scputimes_user, scputimes_system, scputimes_idle, scputimes_steal) values (vid, vtelemetry_id, vconsumption_timestamp, vscputimes_user, vscputimes_system, vscputimes_idle, vscputimes_steal);
 end if;
 return vid;
end;
create function inserttelemetrydisk (vtelemetry_id integer, vconsumption_timestamp varchar(30), vsdiskio_read_bytes varchar(30), vsdiskio_write_bytes varchar(30), vsdiskio_busy_time varchar(30), vsswap_total varchar(30), vsswap_used varchar(30))
returns integer
begin
 declare vid integer;
 select id into vid from telemetry_disk where consumption_timestamp=vconsumption_timestamp;
 if(vid is null) then
 select next value for "telemetry_disk_id_seq" into vid;
 insert into telemetry_disk(id, telemetry_id, consumption_timestamp, sdiskio_read_bytes, sdiskio_write_bytes, sdiskio_busy_time, sswap_total, sswap_used) values (vid, vtelemetry_id, vconsumption_timestamp, vsdiskio_read_bytes, vsdiskio_write_bytes, vsdiskio_busy_time, vsswap_total, vsswap_used);
 end if;
 return vid;
end;
create function inserttelemetrymemory (vtelemetry_id integer, vconsumption_timestamp varchar(30), vsvmem_total varchar(30), vsvmem_available varchar(30), vsvmem_used varchar(30))
returns integer
begin
 declare vid integer;
 select id into vid from telemetry_memory where consumption_timestamp=vconsumption_timestamp;
 if(vid is null) then
 select next value for "telemetry_memory_id_seq" into vid;
 insert into telemetry_memory(id, telemetry_id, consumption_timestamp, svmem_total , svmem_available, svmem_used) values (vid, vtelemetry_id, vconsumption_timestamp, vsvmem_total , vsvmem_available, vsvmem_used);
 end if;
 return vid;
end;
create function inserttelemetrynetwork (vtelemetry_id integer, vconsumption_timestamp varchar(30), vconsumption_value varchar(30))
returns integer
begin
 declare vid integer;
 select id into vid from telemetry_network where consumption_timestamp=vconsumption_timestamp;
 if(vid is null) then
 select next value for "telemetry_network_id_seq" into vid;
 insert into telemetry_network(id, telemetry_id, consumption_timestamp, consumption_value) values (vid, vtelemetry_id, vconsumption_timestamp, vconsumption_value);
 end if;
 return vid;
end;