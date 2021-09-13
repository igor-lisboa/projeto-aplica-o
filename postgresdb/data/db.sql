START TRANSACTION;
CREATE TABLE "public"."user_table" (
	"id"    SERIAL,
	"name"  VARCHAR(50)   NOT NULL,
	"email" VARCHAR(50)   NOT NULL,
	CONSTRAINT "user_table_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."physical_machine" (
	"id"            SERIAL,
	"name"          VARCHAR(50)   NOT NULL,
	"ip"            VARCHAR(50)   NOT NULL,
	"mac"           VARCHAR(50)   NOT NULL,
	"owner_user_id" INTEGER,
	"ram"           INTEGER       NOT NULL,
	"disk"          INTEGER       NOT NULL,
	CONSTRAINT "physical_machine_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."virtual_machine" (
	"id"                  SERIAL,
	"name"                VARCHAR(50)   NOT NULL,
	"ram"                 INTEGER       NOT NULL,
	"disk"                INTEGER       NOT NULL,
	"physical_machine_id" INTEGER       NOT NULL,
	CONSTRAINT "virtual_machine_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."dataflow" (
	"id"      SERIAL,
	"tag"     VARCHAR(50)   NOT NULL,
	"user_id" INTEGER,
	CONSTRAINT "dataflow_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."program" (
	"id"      SERIAL,
	"name"    VARCHAR(200)  NOT NULL,
	"version" VARCHAR(50)   NOT NULL,
	CONSTRAINT "program_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."data_transformation" (
	"id"         SERIAL,
	"df_id"      INTEGER       NOT NULL,
	"tag"        VARCHAR(50)   NOT NULL,
	"program_id" INTEGER,
	CONSTRAINT "data_transformation_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."dataflow_version" (
	"version" SERIAL,
	"df_id"   INTEGER       NOT NULL,
	CONSTRAINT "dataflow_version_version_pkey" PRIMARY KEY ("version")
);
CREATE TABLE "public"."use_program" (
	"dt_id"      INTEGER       NOT NULL,
	"program_id" INTEGER       NOT NULL,
	CONSTRAINT "use_program_dt_id_program_id_pkey" PRIMARY KEY ("dt_id", "program_id")
);
CREATE TABLE "public"."data_set" (
	"id"    SERIAL,
	"df_id" INTEGER       NOT NULL,
	"tag"   VARCHAR(5000) NOT NULL,
	CONSTRAINT "data_set_id_pkey" PRIMARY KEY ("id")
);CREATE TABLE "public"."data_dependency" (
	"id"             SERIAL,
	"previous_dt_id" INTEGER,
	"next_dt_id"     INTEGER,
	"ds_id"          INTEGER       NOT NULL,
	CONSTRAINT "data_dependency_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."extractor" (
	"id"        SERIAL,
	"ds_id"     INTEGER       NOT NULL,
	"tag"       VARCHAR(20)   NOT NULL,
	"cartridge" VARCHAR(20)   NOT NULL,
	"extension" VARCHAR(20)   NOT NULL,
	CONSTRAINT "extractor_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."extractor_combination" (
	"id"           SERIAL,
	"ds_id"        INTEGER       NOT NULL,
	"outer_ext_id" INTEGER       NOT NULL,
	"inner_ext_id" INTEGER       NOT NULL,
	"keys"         VARCHAR(100)  NOT NULL,
	"key_types"    VARCHAR(100)  NOT NULL,
	CONSTRAINT "extractor_combination_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."attribute" (
	"id"          SERIAL,
	"ds_id"        INTEGER       NOT NULL,
	"extractor_id" INTEGER,
	"name"         VARCHAR(30),
	"type"         VARCHAR(15),
	CONSTRAINT "attribute_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."task" (
	"id"               SERIAL,
	"identifier"         INTEGER       NOT NULL,
	"df_version"         INTEGER       NOT NULL,
	"dt_id"              INTEGER       NOT NULL,
	"status"             VARCHAR(10),
	"workspace"          VARCHAR(5000),
	"computing_resource" VARCHAR(100),
	"output_msg"         TEXT,
	"error_msg"          TEXT,
	CONSTRAINT "task_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."file_type" (
	"id"      SERIAL,
	"name" VARCHAR(200)  NOT NULL,
	CONSTRAINT "file_type_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."file" (
	"id"          SERIAL,
	"name"         VARCHAR(200)  NOT NULL,
	"path"         VARCHAR(5000) NOT NULL,
	"id_file_type" INTEGER       NOT NULL,
	CONSTRAINT "file_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."performance" (
	"id"       SERIAL,
	"task_id"     INTEGER       NOT NULL,
	"subtask_id"  INTEGER,
	"method"      VARCHAR(30),
	"description" VARCHAR(200),
	"starttime"   VARCHAR(30),
	"endtime"     VARCHAR(30),
	"invocation"  TEXT,
	CONSTRAINT "performance_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."dataflow_execution" (
	"id"                SERIAL,
	"execution_datetime"  VARCHAR(30)   NOT NULL,
	"df_id"               INTEGER       NOT NULL,
	"physical_machine_id" INTEGER,
	"virtual_machine_id"  INTEGER,
	CONSTRAINT "dataflow_execution_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."data_transformation_execution" (
	"id"                   SERIAL,
	"dataflow_execution_id"  INTEGER       NOT NULL,
	"data_transformation_id" INTEGER       NOT NULL,
	"execution_datetime"     VARCHAR(30)   NOT NULL,
	CONSTRAINT "data_transformation_execution_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."file_transformation_execution" (
	"id"                             SERIAL,
	"file_id"                          INTEGER       NOT NULL,
	"generation_datetime"              VARCHAR(30)   NOT NULL,
	"last_modification_datetime"       VARCHAR(30)   NOT NULL,
	"data_transformation_execution_id" INTEGER       NOT NULL,
	CONSTRAINT "file_transformation_execution_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."epoch" (
	"id"                       SERIAL,
	"value"                            VARCHAR(100)  NOT NULL,
	"elapsed_time"                     DECIMAL(10,2),
	"loss"                             DECIMAL(10,2),
	"accuracy"                         DECIMAL(10,2),
	"epoch_timestamp"                  VARCHAR(30)   NOT NULL,
	"task_id"                          INTEGER,
	"data_transformation_execution_id" INTEGER       NOT NULL,
	CONSTRAINT "epoch_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."telemetry" (
	"id"                      SERIAL,
	"task_id"                          INTEGER       NOT NULL,
	"captured_timestamp"               VARCHAR(30),
	"captured_interval"                VARCHAR(30),
	"data_transformation_execution_id" INTEGER       NOT NULL,
	CONSTRAINT "telemetry_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."telemetry_cpu" (
	"id"                SERIAL,
	"telemetry_id"          INTEGER       NOT NULL,
	"consumption_timestamp" VARCHAR(30),
	"scputimes_user"        VARCHAR(30),
	"scputimes_system"      VARCHAR(30),
	"scputimes_idle"        VARCHAR(30),
	"scputimes_steal"       VARCHAR(30),
	CONSTRAINT "telemetry_cpu_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."telemetry_disk" (
	"id"               SERIAL,
	"telemetry_id"          INTEGER       NOT NULL,
	"consumption_timestamp" VARCHAR(30),
	"sdiskio_read_bytes"    VARCHAR(30),
	"sdiskio_write_bytes"   VARCHAR(30),
	"sdiskio_busy_time"     VARCHAR(30),
	"sswap_total"           VARCHAR(30),
	"sswap_used"            VARCHAR(30),
	CONSTRAINT "telemetry_disk_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."telemetry_network" (
	"id"              SERIAL,
	"telemetry_id"          INTEGER       NOT NULL,
	"consumption_timestamp" VARCHAR(30),
	"consumption_value"     VARCHAR(30),
	CONSTRAINT "telemetry_network_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."telemetry_memory" (
	"id"                SERIAL,
	"telemetry_id"          INTEGER       NOT NULL,
	"consumption_timestamp" VARCHAR(30),
	"svmem_total"           VARCHAR(30),
	"svmem_available"       VARCHAR(30),
	"svmem_used"            VARCHAR(30),
	CONSTRAINT "telemetry_memory_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_ivalidationmodule_raxml" (
	"id"                           SERIAL,
	"validationmodule_raxml_task_id" INTEGER,
	"alignmt"                        VARCHAR(100000),
	"trimmer"                        VARCHAR(100000),
	"program"                        VARCHAR(100000),
	CONSTRAINT "ds_ivalidationmodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_ovalidationmodule_raxml" (
	"id"                         SERIAL,
	"validationmodule_raxml_task_id" INTEGER,
	"alignmt"                        VARCHAR(100000),
	"trimmer"                        VARCHAR(100000),
	"program"                        VARCHAR(100000),
	CONSTRAINT "ds_ovalidationmodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_iremovepipemodule_raxml" (
	"id"                           SERIAL,
	"removepipemodule_raxml_task_id" INTEGER,
	"inputfile"                      VARCHAR(100000),
	CONSTRAINT "ds_iremovepipemodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_oremovepipemodule_raxml" (
	"id"                           SERIAL,
	"removepipemodule_raxml_task_id" INTEGER,
	"cleanedfile"                    VARCHAR(100000),
	CONSTRAINT "ds_oremovepipemodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_ialignmentmodule_raxml" (
	"id"                           SERIAL,
	"alignmentmodule_raxml_task_id" INTEGER,
	"directory"                     VARCHAR(100000),
	"cleaned_seq"                   VARCHAR(100000),
	CONSTRAINT "ds_ialignmentmodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_oalignmentmodule_raxml" (
	"id"                          SERIAL,
	"alignmentmodule_raxml_task_id" INTEGER,
	"alignmenttype"                 VARCHAR(100000),
	"directory"                     VARCHAR(100000),
	"alignedcode"                   VARCHAR(100000),
	CONSTRAINT "ds_oalignmentmodule_raxml_id_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "public"."ds_iconvertermodule_raxml" (
	"id"                            SERIAL,
	"convertermodule_raxml_task_id" INTEGER,
	"dirin"                         VARCHAR(100000),
	"inputfile"                     VARCHAR(100000),
	"trimmer"                       VARCHAR(100000),
	CONSTRAINT "ds_iconvertermodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_oconvertermodule_raxml" (
	"id"                           SERIAL,
	"convertermodule_raxml_task_id" INTEGER,
	"nxs_file"                      VARCHAR(100000),
	"phy_file"                      VARCHAR(100000),
	CONSTRAINT "ds_oconvertermodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_imodelgeneratormodule_raxml" (
	"id"                               SERIAL,
	"modelgeneratormodule_raxml_task_id" INTEGER,
	"alignedfile"                        VARCHAR(100000),
	CONSTRAINT "ds_imodelgeneratormodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_omodelgeneratormodule_raxml" (
	"id"                                SERIAL,
	"modelgeneratormodule_raxml_task_id" INTEGER,
	"model"                              VARCHAR(100000),
	"model_file"                         VARCHAR(100000),
	CONSTRAINT "ds_omodelgeneratormodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_iprogramexecutemodule_raxml" (
	"id"                               SERIAL,
	"programexecutemodule_raxml_task_id" INTEGER,
	"program"                            VARCHAR(100000),
	CONSTRAINT "ds_iprogramexecutemodule_raxml_id_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "public"."ds_oprogramexecutemodule_raxml" (
	"id"                                SERIAL,
	"programexecutemodule_raxml_task_id" INTEGER,
	"program"                            VARCHAR(100000),
	"mbout"                              VARCHAR(100000),
	"param_mbayes"                       VARCHAR(100000),
	"nxs_ckp"                            VARCHAR(100000),
	"con_tre"                            VARCHAR(100000),
	"parts"                              VARCHAR(100000),
	CONSTRAINT "ds_oprogramexecutemodule_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_itelemetry_raxml" (
	"id"                         SERIAL,
	"telemetrymodule_raxml_task_id" INTEGER,
	"test"                          DECIMAL,
	CONSTRAINT "ds_itelemetry_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_otelemetry_raxml" (
	"id"                          SERIAL,
	"telemetrymodule_raxml_task_id" INTEGER,
	"timestamp"                     VARCHAR(100000),
	"scputimes_nice"                VARCHAR(100000),
	"svmem_percent"                 VARCHAR(100000),
	"sdiskio_read_time"             VARCHAR(100000),
	"sdiskio_write_time"            VARCHAR(100000),
	CONSTRAINT "ds_otelemetry_raxml_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_ivalidationmodule_mrb" (
	"id"                          SERIAL,
	"validationmodule_mrb_task_id" INTEGER,
	"alignmt"                      VARCHAR(100000),
	"trimmer"                      VARCHAR(100000),
	"program"                      VARCHAR(100000),
	CONSTRAINT "ds_ivalidationmodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_ovalidationmodule_mrb" (
	"id"                         SERIAL,
	"validationmodule_mrb_task_id" INTEGER,
	"alignmt"                      VARCHAR(100000),
	"trimmer"                      VARCHAR(100000),
	"program"                      VARCHAR(100000),
	CONSTRAINT "ds_ovalidationmodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_iremovepipemodule_mrb" (
	"id"                          SERIAL,
	"removepipemodule_mrb_task_id" INTEGER,
	"inputfile"                    VARCHAR(100000),
	CONSTRAINT "ds_iremovepipemodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_oremovepipemodule_mrb" (
	"id"                        SERIAL,
	"removepipemodule_mrb_task_id" INTEGER,
	"cleanedfile"                  VARCHAR(100000),
	CONSTRAINT "ds_oremovepipemodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_ialignmentmodule_mrb" (
	"id"                       SERIAL,
	"alignmentmodule_mrb_task_id" INTEGER,
	"directory"                   VARCHAR(100000),
	"cleaned_seq"                 VARCHAR(100000),
	CONSTRAINT "ds_ialignmentmodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_oalignmentmodule_mrb" (
	"id"                        SERIAL,
	"alignmentmodule_mrb_task_id" INTEGER,
	"alignmenttype"               VARCHAR(100000),
	"directory"                   VARCHAR(100000),
	"alignedcode"                 VARCHAR(100000),
	CONSTRAINT "ds_oalignmentmodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_iconvertermodule_mrb" (
	"id"                        SERIAL,
	"convertermodule_mrb_task_id" INTEGER,
	"dirin"                       VARCHAR(100000),
	"inputfile"                   VARCHAR(100000),
	"trimmer"                     VARCHAR(100000),
	CONSTRAINT "ds_iconvertermodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_oconvertermodule_mrb" (
	"id"                       SERIAL,
	"convertermodule_mrb_task_id" INTEGER,
	"nxs_file"                    VARCHAR(100000),
	"phy_file"                    VARCHAR(100000),
	CONSTRAINT "ds_oconvertermodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_imodelgeneratormodule_mrb" (
	"id"                        SERIAL,
	"modelgeneratormodule_mrb_task_id" INTEGER,
	"alignedfile"                      VARCHAR(100000),
	CONSTRAINT "ds_imodelgeneratormodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_omodelgeneratormodule_mrb" (
	"id"                            SERIAL,
	"modelgeneratormodule_mrb_task_id" INTEGER,
	"model"                            VARCHAR(100000),
	"model_file"                       VARCHAR(100000),
	CONSTRAINT "ds_omodelgeneratormodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_iprogramexecutemodule_mrb" (
	"id"                           SERIAL,
	"programexecutemodule_mrb_task_id" INTEGER,
	"program"                          VARCHAR(100000),
	CONSTRAINT "ds_iprogramexecutemodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_oprogramexecutemodule_mrb" (
	"id"                              SERIAL,
	"programexecutemodule_mrb_task_id" INTEGER,
	"program"                          VARCHAR(100000),
	"mbout"                            VARCHAR(100000),
	"param_mbayes"                     VARCHAR(100000),
	"nxs_ckp"                          VARCHAR(100000),
	"con_tre"                          VARCHAR(100000),
	"parts"                            VARCHAR(100000),
	CONSTRAINT "ds_oprogramexecutemodule_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_itelemetry_mrb" (
	"id"                        SERIAL,
	"telemetrymodule_mrb_task_id" INTEGER,
	"test"                        DECIMAL,
	CONSTRAINT "ds_itelemetry_mrb_id_pkey" PRIMARY KEY ("id")
);
CREATE TABLE "public"."ds_otelemetry_mrb" (
	"id"                      SERIAL,
	"telemetrymodule_mrb_task_id" INTEGER,
	"timestamp"                   VARCHAR(100000),
	"scputimes_nice"              VARCHAR(100000),
	"svmem_percent"               VARCHAR(100000),
	"sdiskio_read_time"           VARCHAR(100000),
	"sdiskio_write_time"          VARCHAR(100000),
	CONSTRAINT "ds_otelemetry_mrb_id_pkey" PRIMARY KEY ("id")
);
COMMIT;