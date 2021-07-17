create view ivalidationmodule_raxml(id, validationmodule_raxml_task_id, alignmt, trimmer, program) as
select ds.id, ds.validationmodule_raxml_task_id, ds.alignmt, ds.trimmer, ds.program
 from ds_ivalidationmodule_raxml as ds
;
create view ovalidationmodule_raxml(id, validationmodule_raxml_task_id, alignmt, trimmer, program) as
select ds.id, ds.validationmodule_raxml_task_id, ds.alignmt, ds.trimmer, ds.program
 from ds_ovalidationmodule_raxml as ds
;
create view iremovepipemodule_raxml(id, removepipemodule_raxml_task_id, inputfile) as
select ds.id, ds.removepipemodule_raxml_task_id, ds.inputfile
 from ds_iremovepipemodule_raxml as ds
;
create view oremovepipemodule_raxml(id, removepipemodule_raxml_task_id, cleanedfile) as
select ds.id, ds.removepipemodule_raxml_task_id, ds.cleanedfile
 from ds_oremovepipemodule_raxml as ds
;
create view ialignmentmodule_raxml(id, alignmentmodule_raxml_task_id, directory, cleaned_seq) as
select ds.id, ds.alignmentmodule_raxml_task_id, ds.directory, ds.cleaned_seq
 from ds_ialignmentmodule_raxml as ds
;
create view oalignmentmodule_raxml(id, alignmentmodule_raxml_task_id, alignmenttype, directory, alignedcode) as
select ds.id, ds.alignmentmodule_raxml_task_id, ds.alignmenttype, ds.directory, ds.alignedcode
 from ds_oalignmentmodule_raxml as ds
;
create view iconvertermodule_raxml(id, convertermodule_raxml_task_id, dirin, inputfile, trimmer) as
select ds.id, ds.convertermodule_raxml_task_id, ds.dirin, ds.inputfile, ds.trimmer
 from ds_iconvertermodule_raxml as ds
;
create view oconvertermodule_raxml(id, convertermodule_raxml_task_id, nxs_file, phy_file) as
select ds.id, ds.convertermodule_raxml_task_id, ds.nxs_file, ds.phy_file
 from ds_oconvertermodule_raxml as ds
;
create view imodelgeneratormodule_raxml(id, modelgeneratormodule_raxml_task_id, alignedfile) as
select ds.id, ds.modelgeneratormodule_raxml_task_id, ds.alignedfile
 from ds_imodelgeneratormodule_raxml as ds
;
create view omodelgeneratormodule_raxml(id, modelgeneratormodule_raxml_task_id, model, model_file) as
select ds.id, ds.modelgeneratormodule_raxml_task_id, ds.model, ds.model_file
 from ds_omodelgeneratormodule_raxml as ds
;
create view iprogramexecutemodule_raxml(id, programexecutemodule_raxml_task_id, program) as
select ds.id, ds.programexecutemodule_raxml_task_id, ds.program
 from ds_iprogramexecutemodule_raxml as ds
;
create view oprogramexecutemodule_raxml(id, programexecutemodule_raxml_task_id, program, mbout, param_mbayes, nxs_ckp, con_tre, parts) as
select ds.id, ds.programexecutemodule_raxml_task_id, ds.program, ds.mbout, ds.param_mbayes, ds.nxs_ckp, ds.con_tre, ds.parts
 from ds_oprogramexecutemodule_raxml as ds
;
create view itelemetry_raxml(id, telemetrymodule_raxml_task_id, test) as
select ds.id, ds.telemetrymodule_raxml_task_id, ds.test
 from ds_itelemetry_raxml as ds
;
create view otelemetry_raxml(id, telemetrymodule_raxml_task_id, timestamp, scputimes_nice, svmem_percent, sdiskio_read_time, sdiskio_write_time) as
select ds.id, ds.telemetrymodule_raxml_task_id, ds.timestamp, ds.scputimes_nice, ds.svmem_percent, ds.sdiskio_read_time, ds.sdiskio_write_time
 from ds_otelemetry_raxml as ds
;
create view ivalidationmodule_mrb(id, validationmodule_mrb_task_id, alignmt, trimmer, program) as
select ds.id, ds.validationmodule_mrb_task_id, ds.alignmt, ds.trimmer, ds.program
 from ds_ivalidationmodule_mrb as ds
;
create view ovalidationmodule_mrb(id, validationmodule_mrb_task_id, alignmt, trimmer, program) as
select ds.id, ds.validationmodule_mrb_task_id, ds.alignmt, ds.trimmer, ds.program
 from ds_ovalidationmodule_mrb as ds
;
create view iremovepipemodule_mrb(id, removepipemodule_mrb_task_id, inputfile) as
select ds.id, ds.removepipemodule_mrb_task_id, ds.inputfile
 from ds_iremovepipemodule_mrb as ds
;
create view oremovepipemodule_mrb(id, removepipemodule_mrb_task_id, cleanedfile) as
select ds.id, ds.removepipemodule_mrb_task_id, ds.cleanedfile
 from ds_oremovepipemodule_mrb as ds
;
create view ialignmentmodule_mrb(id, alignmentmodule_mrb_task_id, directory, cleaned_seq) as
select ds.id, ds.alignmentmodule_mrb_task_id, ds.directory, ds.cleaned_seq
 from ds_ialignmentmodule_mrb as ds
;
create view oalignmentmodule_mrb(id, alignmentmodule_mrb_task_id, alignmenttype, directory, alignedcode) as
select ds.id, ds.alignmentmodule_mrb_task_id, ds.alignmenttype, ds.directory, ds.alignedcode
 from ds_oalignmentmodule_mrb as ds
;
create view iconvertermodule_mrb(id, convertermodule_mrb_task_id, dirin, inputfile, trimmer) as
select ds.id, ds.convertermodule_mrb_task_id, ds.dirin, ds.inputfile, ds.trimmer
 from ds_iconvertermodule_mrb as ds
;
create view oconvertermodule_mrb(id, convertermodule_mrb_task_id, nxs_file, phy_file) as
select ds.id, ds.convertermodule_mrb_task_id, ds.nxs_file, ds.phy_file
 from ds_oconvertermodule_mrb as ds
;
create view imodelgeneratormodule_mrb(id, modelgeneratormodule_mrb_task_id, alignedfile) as
select ds.id, ds.modelgeneratormodule_mrb_task_id, ds.alignedfile
 from ds_imodelgeneratormodule_mrb as ds
;
create view omodelgeneratormodule_mrb(id, modelgeneratormodule_mrb_task_id, model, model_file) as
select ds.id, ds.modelgeneratormodule_mrb_task_id, ds.model, ds.model_file
 from ds_omodelgeneratormodule_mrb as ds
;
create view iprogramexecutemodule_mrb(id, programexecutemodule_mrb_task_id, program) as
select ds.id, ds.programexecutemodule_mrb_task_id, ds.program
 from ds_iprogramexecutemodule_mrb as ds
;
create view oprogramexecutemodule_mrb(id, programexecutemodule_mrb_task_id, program, mbout, param_mbayes, nxs_ckp, con_tre, parts) as
select ds.id, ds.programexecutemodule_mrb_task_id, ds.program, ds.mbout, ds.param_mbayes, ds.nxs_ckp, ds.con_tre, ds.parts
 from ds_oprogramexecutemodule_mrb as ds
;
create view itelemetry_mrb(id, telemetrymodule_mrb_task_id, test) as
select ds.id, ds.telemetrymodule_mrb_task_id, ds.test
 from ds_itelemetry_mrb as ds
;
create view otelemetry_mrb(id, telemetrymodule_mrb_task_id, timestamp, scputimes_nice, svmem_percent, sdiskio_read_time, sdiskio_write_time) as
select ds.id, ds.telemetrymodule_mrb_task_id, ds.timestamp, ds.scputimes_nice, ds.svmem_percent, ds.sdiskio_read_time, ds.sdiskio_write_time
 from ds_otelemetry_mrb as ds
;