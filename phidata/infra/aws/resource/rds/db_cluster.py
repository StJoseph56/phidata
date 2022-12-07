from pathlib import Path
from typing import Optional, Any, Dict, List, Literal, Union

from phidata.infra.aws.api_client import AwsApiClient
from phidata.infra.aws.resource.base import AwsResource
from phidata.infra.aws.resource.cloudformation.stack import CloudFormationStack
from phidata.infra.aws.resource.rds.db_instance import DbInstance
from phidata.infra.aws.resource.rds.db_subnet_group import DbSubnetGroup
from phidata.utils.cli_console import print_info, print_error, print_warning
from phidata.utils.log import logger


class DbCluster(AwsResource):
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html
    """

    resource_type = "DbCluster"
    service_name = "rds"

    # Name of the cluster.
    name: str
    # The name of the database engine to be used for this DB cluster.
    engine: Union[
        str, Literal["aurora", "aurora-mysql", "aurora-postgresql", "mysql", "postgres"]
    ]
    # DbInstances to add to this cluster
    db_instances: Optional[List[DbInstance]] = None
    # The version number of the database engine to use.
    # For valid engine_version values, refer to
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.create_db_cluster
    engine_version: Optional[str] = None

    # The port number on which the instances in the DB cluster accept connections.
    # RDS for MySQL and Aurora MySQL
    # - Default: 3306
    # - Valid values: 1150-65535
    # RDS for PostgreSQL and Aurora PostgreSQL
    # - Default: 5432
    # - Valid values: 1150-65535
    port: Optional[int] = None
    # The name of the master user for the DB cluster.
    # Constraints:
    #   Must be 1 to 16 letters or numbers.
    #   First character must be a letter.
    #   Can't be a reserved word for the chosen database engine.
    # Provide MASTER_USERNAME here or as MASTER_USERNAME in secrets_file
    master_username: Optional[str] = None
    # The password for the master database user. This password can contain any printable ASCII character
    # except "/", """, or "@".
    # Constraints: Must contain from 8 to 41 characters.
    # Provide MASTER_USER_PASSWORD here or as MASTER_USER_PASSWORD in secrets_file
    master_user_password: Optional[str] = None
    # Read secrets from a file in yaml format
    secrets_file: Optional[Path] = None

    # A list of Availability Zones (AZs) where DB instances in the DB cluster can be created.
    # Valid for: Aurora DB clusters only
    availability_zones: Optional[List[str]] = None
    # The number of days for which automated backups are retained.
    # Default: 1
    # Constraints: Must be a value from 1 to 35
    # Valid for: Aurora DB clusters and Multi-AZ DB clusters
    backup_retention_period: Optional[int] = None
    # A value that indicates that the DB cluster should be associated with the specified CharacterSet.
    # Valid for: Aurora DB clusters only
    character_set_name: Optional[str] = None
    # The name for your database of up to 64 alphanumeric characters.
    # If you do not provide a name, Amazon RDS doesn't create a database in the DB cluster you are creating.
    # Provide DATABASE_NAME here or as DATABASE_NAME in secrets_file
    # Valid for: Aurora DB clusters and Multi-AZ DB clusters
    database_name: Optional[str] = None
    # The DB cluster identifier. This parameter is stored as a lowercase string.
    # If None, use the name as the db_cluster_identifier
    # Constraints:
    #   Must contain from 1 to 63 letters, numbers, or hyphens.
    #   First character must be a letter.
    #   Can't end with a hyphen or contain two consecutive hyphens.
    # Example: my-cluster1
    # Valid for: Aurora DB clusters and Multi-AZ DB clusters
    db_cluster_identifier: Optional[str] = None
    # The name of the DB cluster parameter group to associate with this DB cluster.
    # If you do not specify a value, then the default DB cluster parameter group for the specified
    # DB engine and version is used.
    # Constraints: If supplied, must match the name of an existing DB cluster parameter group.
    db_cluster_parameter_group_name: Optional[str] = None

    ## Networking
    # A list of EC2 VPC security groups to associate with this DB cluster.
    vpc_security_group_ids: Optional[List[str]] = None
    # If vpc_security_group_ids is None,
    # Read the security_group_id from vpc_stack
    vpc_stack: Optional[CloudFormationStack] = None

    # A DB subnet group to associate with this DB cluster.
    # This setting is required to create a Multi-AZ DB cluster.
    # Constraints: Must match the name of an existing DBSubnetGroup. Must not be default.
    db_subnet_group_name: Optional[str] = None
    # If db_subnet_group_name is None,
    # Read the db_subnet_group_name from db_subnet_group
    db_subnet_group: Optional[DbSubnetGroup] = None

    # A value that indicates that the DB cluster should be associated with the specified option group.
    option_group_name: Optional[str] = None
    # The daily time range during which automated backups are created if automated backups are enabled
    # using the BackupRetentionPeriod parameter.
    # The default is a 30-minute window selected at random from an 8-hour block of time for each
    # Amazon Web Services Region.
    # Constraints:
    #   Must be in the format hh24:mi-hh24:mi .
    #   Must be in Universal Coordinated Time (UTC).
    #   Must not conflict with the preferred maintenance window.
    #   Must be at least 30 minutes.
    preferred_backup_window: Optional[str] = None
    # The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC).
    # Format: ddd:hh24:mi-ddd:hh24:mi
    # The default is a 30-minute window selected at random from an 8-hour block of time for each
    # Amazon Web Services Region, occurring on a random day of the week.
    # Valid Days: Mon, Tue, Wed, Thu, Fri, Sat, Sun.
    # Constraints: Minimum 30-minute window.
    preferred_maintenance_window: Optional[str] = None
    # The Amazon Resource Name (ARN) of the source DB instance or DB cluster
    # if this DB cluster is created as a read replica.
    replication_source_identifier: Optional[str] = None
    # Tags to assign to the DB cluster.
    tags: Optional[List[Dict[str, str]]] = None
    # A value that indicates whether the DB cluster is encrypted.
    storage_encrypted: Optional[bool] = None
    # The Amazon Web Services KMS key identifier for an encrypted DB cluster.
    kms_key_id: Optional[str] = None
    pre_signed_url: Optional[str] = None
    # A value that indicates whether to enable mapping of Amazon Web Services Identity and Access Management (IAM)
    # accounts to database accounts. By default, mapping isn't enabled.
    enable_iam_database_authentication: Optional[bool] = None
    # The target backtrack window, in seconds. To disable backtracking, set this value to 0.
    # Default: 0
    backtrack_window: Optional[int] = None
    # The list of log types that need to be enabled for exporting to CloudWatch Logs.
    # The values in the list depend on the DB engine being used.
    # RDS for MySQL: Possible values are error , general , and slowquery .
    # RDS for PostgreSQL: Possible values are postgresql and upgrade .
    # Aurora MySQL: Possible values are audit , error , general , and slowquery .
    # Aurora PostgreSQL: Possible value is postgresql .
    enable_cloudwatch_logs_exports: Optional[List[str]] = None
    # The DB engine mode of the DB cluster,
    # either provisioned , serverless , parallelquery , global , or multimaster .
    engine_mode: Optional[
        Literal["provisioned", "serverless", "parallelquery", "global", "multimaster"]
    ] = None
    # For DB clusters in serverless DB engine mode, the scaling properties of the DB cluster.
    scaling_configuration: Optional[Dict[str, Any]] = None
    # A value that indicates whether the DB cluster has deletion protection enabled.
    # The database can't be deleted when deletion protection is enabled. By default, deletion protection isn't enabled.
    deletion_protection: Optional[bool] = None
    # The global cluster ID of an Aurora cluster that becomes the primary cluster in the new global database cluster.
    global_cluster_identifier: Optional[str] = None
    # A value that indicates whether to enable the HTTP endpoint for an Aurora Serverless v1 DB cluster.
    # By default, the HTTP endpoint is disabled.
    # When enabled, the HTTP endpoint provides a connectionless web service
    # API for running SQL queries on the Aurora Serverless v1 DB cluster.
    # You can also query your database from inside the RDS console with the query editor.
    enable_http_endpoint: Optional[bool] = None
    # A value that indicates whether to copy all tags from the DB cluster to snapshots of the DB cluster.
    # The default is not to copy them.
    copy_tags_to_snapshot: Optional[bool] = None
    # The Active Directory directory ID to create the DB cluster in.
    # For Amazon Aurora DB clusters, Amazon RDS can use Kerberos authentication to authenticate users that connect to
    # the DB cluster.
    domain: Optional[str] = None
    # Specify the name of the IAM role to be used when making API calls to the Directory Service.
    domain_iam_role_name: Optional[str] = None
    enable_global_write_forwarding: Optional[bool] = None

    # Compute and memory capacity of each DB instance in the Multi-AZ DB cluster, for example db.m6g.xlarge.
    # Not all DB instance classes are available in all Amazon Web Services Regions, or for all database engines.
    # This setting is required to create a Multi-AZ DB cluster.
    db_instance_class: Optional[str] = None
    # The amount of storage in gibibytes (GiB) to allocate to each DB instance in the Multi-AZ DB cluster.
    allocated_storage: Optional[int] = None
    # Specifies the storage type to be associated with the DB cluster.
    # This setting is required to create a Multi-AZ DB cluster.
    # Valid values: io1
    # When specified, a value for the Iops parameter is required.
    # Default: io1
    storage_type: Optional[str] = None
    # The amount of Provisioned IOPS (input/output operations per second) to be initially allocated for each DB
    # instance in the Multi-AZ DB cluster.
    iops: Optional[int] = None
    # A value that indicates whether the DB cluster is publicly accessible.
    # When the DB cluster is publicly accessible, its Domain Name System (DNS) endpoint resolves to the private IP
    # address from within the DB cluster's virtual private cloud (VPC). It resolves to the public IP address from
    # outside of the DB cluster's VPC. Access to the DB cluster is ultimately controlled by the security group it uses.
    # That public access isn't permitted if the security group assigned to the DB cluster doesn't permit it.
    # When the DB cluster isn't publicly accessible, it is an internal DB cluster with a DNS name
    # that resolves to a private IP address.
    publicly_accessible: Optional[bool] = None
    # A value that indicates whether minor engine upgrades are applied automatically to the DB cluster during the
    # maintenance window. By default, minor engine upgrades are applied automatically.
    auto_minor_version_upgrade: Optional[bool] = None
    # The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB cluster.
    # To turn off collecting Enhanced Monitoring metrics, specify 0. The default is 0.
    # If MonitoringRoleArn is specified, also set MonitoringInterval to a value other than 0.
    # Valid Values: 0, 1, 5, 10, 15, 30, 60
    monitoring_interval: Optional[int] = None
    # The Amazon Resource Name (ARN) for the IAM role that permits RDS to send
    # Enhanced Monitoring metrics to Amazon CloudWatch Logs.
    monitoring_role_arn: Optional[str] = None
    enable_performance_insights: Optional[bool] = None
    performance_insights_kms_key_id: Optional[str] = None
    performance_insights_retention_period: Optional[int] = None
    # Contains the scaling configuration of an Aurora Serverless v2 DB cluster.
    serverless_v2_scaling_configuration: Dict[str, Any] = {
        "MinCapacity": 0.5,
        "MaxCapacity": 8,
    }
    # The network type of the DB cluster.
    # Valid values:
    # - IPV4
    # - DUAL
    # The network type is determined by the DBSubnetGroup specified for the DB cluster.
    # A DBSubnetGroup can support only the IPv4 protocol or the IPv4 and the IPv6 protocols (DUAL ).
    network_type: Optional[str] = None
    # Reserved for future use.
    db_system_id: Optional[str] = None
    # The ID of the region that contains the source for the db cluster.
    source_region: Optional[str] = None

    # Skip the creation of a final DB cluster snapshot before the DB cluster is deleted.
    # If skip_final_snapshot = True, no DB cluster snapshot is created.
    # If skip_final_snapshot = None, a DB cluster snapshot is created before the DB cluster is deleted.
    #
    # You must specify a FinalDBSnapshotIdentifier parameter
    # if skip_final_snapshot = None.
    skip_final_snapshot: Optional[bool] = True
    final_db_snapshot_identifier: Optional[str] = None

    # Cache secret_data
    cached_secret_data: Optional[Dict[str, Any]] = None

    def get_db_cluster_identifier(self):
        return self.db_cluster_identifier or self.name

    def get_secret_data(self) -> Optional[Dict[str, str]]:
        if self.cached_secret_data is not None:
            return self.cached_secret_data

        if self.secrets_file is not None:
            self.cached_secret_data = self.read_yaml_file(self.secrets_file)
        return self.cached_secret_data

    def get_master_username(self) -> Optional[str]:
        master_username = self.master_username
        if master_username is None and self.secrets_file is not None:
            # read from secrets_file
            secret_data = self.get_secret_data()
            if secret_data is not None:
                master_username = secret_data.get("MASTER_USERNAME", master_username)
        return master_username

    def get_master_user_password(self) -> Optional[str]:
        master_user_password = self.master_user_password
        if master_user_password is None and self.secrets_file is not None:
            # read from secrets_file
            secret_data = self.get_secret_data()
            if secret_data is not None:
                master_user_password = secret_data.get(
                    "MASTER_USER_PASSWORD", master_user_password
                )
        return master_user_password

    def get_database_name(self) -> Optional[str]:
        database_name = self.database_name
        if database_name is None and self.secrets_file is not None:
            # read from secrets_file
            secret_data = self.get_secret_data()
            if secret_data is not None:
                database_name = secret_data.get("DATABASE_NAME", database_name)
                if database_name is None:
                    database_name = secret_data.get("DB_NAME", database_name)
        return database_name

    def get_db_name(self) -> Optional[str]:
        # Alias for get_database_name because db_instances use `db_name` and db_clusters use `database_name`
        return self.get_database_name()

    def _create(self, aws_client: AwsApiClient) -> bool:
        """Creates the DbCluster

        Args:
            aws_client: The AwsApiClient for the current cluster
        """
        print_info(f"Creating {self.get_resource_type()}: {self.get_resource_name()}")

        # Step 1: Get the VpcSecurityGroupIds
        vpc_security_group_ids = self.vpc_security_group_ids
        if vpc_security_group_ids is None and self.vpc_stack is not None:
            vpc_stack_sg = self.vpc_stack.get_security_group(aws_client=aws_client)
            if vpc_stack_sg is not None:
                logger.debug(f"Using SecurityGroup: {vpc_stack_sg}")
                vpc_security_group_ids = [vpc_stack_sg]

        # Step 2: Get the DbSubnetGroupName
        db_subnet_group_name = self.db_subnet_group_name
        if db_subnet_group_name is None and self.db_subnet_group is not None:
            db_subnet_group_name = self.db_subnet_group.name
            logger.debug(f"Using DbSubnetGroup: {db_subnet_group_name}")

        # create a dict of args which are not null, otherwise aws type validation fails
        not_null_args: Dict[str, Any] = {}
        if self.availability_zones:
            not_null_args["AvailabilityZones"] = self.availability_zones
        if self.backup_retention_period:
            not_null_args["BackupRetentionPeriod"] = self.backup_retention_period
        if self.character_set_name:
            not_null_args["CharacterSetName"] = self.character_set_name

        database_name = self.get_database_name()
        if database_name:
            not_null_args["DatabaseName"] = database_name

        if self.db_cluster_parameter_group_name:
            not_null_args[
                "DBClusterParameterGroupName"
            ] = self.db_cluster_parameter_group_name

        if vpc_security_group_ids is not None:
            not_null_args["VpcSecurityGroupIds"] = vpc_security_group_ids
        if db_subnet_group_name is not None:
            not_null_args["DBSubnetGroupName"] = db_subnet_group_name

        if self.engine_version:
            not_null_args["EngineVersion"] = self.engine_version
        if self.port:
            not_null_args["Port"] = self.port

        master_username = self.get_master_username()
        if master_username:
            not_null_args["MasterUsername"] = master_username
        master_user_password = self.get_master_user_password()
        if master_user_password:
            not_null_args["MasterUserPassword"] = master_user_password

        if self.option_group_name:
            not_null_args["OptionGroupName"] = self.option_group_name
        if self.preferred_backup_window:
            not_null_args["PreferredBackupWindow"] = self.preferred_backup_window
        if self.preferred_maintenance_window:
            not_null_args[
                "PreferredMaintenanceWindow"
            ] = self.preferred_maintenance_window
        if self.replication_source_identifier:
            not_null_args[
                "ReplicationSourceIdentifier"
            ] = self.replication_source_identifier
        if self.tags:
            not_null_args["Tags"] = self.tags
        if self.storage_encrypted:
            not_null_args["StorageEncrypted"] = self.storage_encrypted
        if self.kms_key_id:
            not_null_args["KmsKeyId"] = self.kms_key_id
        if self.enable_iam_database_authentication:
            not_null_args[
                "EnableIAMDbClusterAuthentication"
            ] = self.enable_iam_database_authentication
        if self.backtrack_window:
            not_null_args["BacktrackWindow"] = self.backtrack_window
        if self.enable_cloudwatch_logs_exports:
            not_null_args[
                "EnableCloudwatchLogsExports"
            ] = self.enable_cloudwatch_logs_exports
        if self.engine_mode:
            not_null_args["EngineMode"] = self.engine_mode
        if self.scaling_configuration:
            not_null_args["ScalingConfiguration"] = self.scaling_configuration
        if self.deletion_protection:
            not_null_args["DeletionProtection"] = self.deletion_protection
        if self.global_cluster_identifier:
            not_null_args["GlobalClusterIdentifier"] = self.global_cluster_identifier
        if self.enable_http_endpoint:
            not_null_args["EnableHttpEndpoint"] = self.enable_http_endpoint
        if self.copy_tags_to_snapshot:
            not_null_args["CopyTagsToSnapshot"] = self.copy_tags_to_snapshot
        if self.domain:
            not_null_args["Domain"] = self.domain
        if self.domain_iam_role_name:
            not_null_args["DomainIAMRoleName"] = self.domain_iam_role_name
        if self.enable_global_write_forwarding:
            not_null_args[
                "EnableGlobalWriteForwarding"
            ] = self.enable_global_write_forwarding
        if self.db_instance_class:
            not_null_args["DBClusterInstanceClass"] = self.db_instance_class
        if self.allocated_storage:
            not_null_args["AllocatedStorage"] = self.allocated_storage
        if self.storage_type:
            not_null_args["StorageType"] = self.storage_type
        if self.iops:
            not_null_args["Iops"] = self.iops
        if self.publicly_accessible:
            not_null_args["PubliclyAccessible"] = self.publicly_accessible
        if self.auto_minor_version_upgrade:
            not_null_args["AutoMinorVersionUpgrade"] = self.auto_minor_version_upgrade
        if self.monitoring_interval:
            not_null_args["MonitoringInterval"] = self.monitoring_interval
        if self.monitoring_role_arn:
            not_null_args["MonitoringRoleArn"] = self.monitoring_role_arn
        if self.enable_performance_insights:
            not_null_args[
                "EnablePerformanceInsights"
            ] = self.enable_performance_insights
        if self.performance_insights_kms_key_id:
            not_null_args[
                "PerformanceInsightsKMSKeyId"
            ] = self.performance_insights_kms_key_id
        if self.performance_insights_retention_period:
            not_null_args[
                "PerformanceInsightsRetentionPeriod"
            ] = self.performance_insights_retention_period
        if self.serverless_v2_scaling_configuration:
            not_null_args[
                "ServerlessV2ScalingConfiguration"
            ] = self.serverless_v2_scaling_configuration
        if self.network_type:
            not_null_args["NetworkType"] = self.network_type
        if self.db_system_id:
            not_null_args["DBSystemId"] = self.db_system_id
        if self.source_region:
            not_null_args["SourceRegion"] = self.source_region

        # Step 3: Create DbCluster
        service_client = self.get_service_client(aws_client)
        try:
            create_response = service_client.create_db_cluster(
                DBClusterIdentifier=self.get_db_cluster_identifier(),
                Engine=self.engine,
                **not_null_args,
            )
            logger.debug(f"DbCluster: {create_response}")
            database_dict = create_response.get("DBCluster", {})

            # Validate database creation
            if database_dict is not None:
                print_info(f"DbCluster created: {self.get_db_cluster_identifier()}")
                self.active_resource = create_response
                return True
        except Exception as e:
            print_error(f"{self.get_resource_type()} could not be created.")
            print_error(e)
        return False

    def post_create(self, aws_client: AwsApiClient) -> bool:

        db_instances_created = []
        if self.db_instances is not None:
            for db_instance in self.db_instances:
                db_instance.db_cluster_identifier = self.get_db_cluster_identifier()
                if db_instance._create(aws_client):  # type: ignore
                    db_instances_created.append(db_instance)

        # Wait for DbCluster to be created
        if self.wait_for_creation:
            try:
                print_info(f"Waiting for {self.get_resource_type()} to be active.")
                waiter = self.get_service_client(aws_client).get_waiter(
                    "db_cluster_available"
                )
                waiter.wait(
                    DBClusterIdentifier=self.get_db_cluster_identifier(),
                    WaiterConfig={
                        "Delay": self.waiter_delay,
                        "MaxAttempts": self.waiter_max_attempts,
                    },
                )
            except Exception as e:
                print_error("Waiter failed.")
                print_error(e)

            # Wait for DbInstances to be created
            for db_instance in db_instances_created:
                db_instance.post_create(aws_client)

        return True

    def _read(self, aws_client: AwsApiClient) -> Optional[Any]:
        """Returns the DbCluster

        Args:
            aws_client: The AwsApiClient for the current cluster
        """
        logger.debug(f"Reading {self.get_resource_type()}: {self.get_resource_name()}")

        from botocore.exceptions import ClientError

        service_client = self.get_service_client(aws_client)
        try:
            db_cluster_identifier = self.get_db_cluster_identifier()
            describe_response = service_client.describe_db_clusters(
                DBClusterIdentifier=db_cluster_identifier
            )
            logger.debug(f"DbCluster: {describe_response}")
            db_clusters_list = describe_response.get("DBClusters", None)

            if db_clusters_list is not None and isinstance(db_clusters_list, list):
                for _db_cluster in db_clusters_list:
                    _cluster_identifier = _db_cluster.get("DBClusterIdentifier", None)
                    if _cluster_identifier == db_cluster_identifier:
                        self.active_resource = _db_cluster
                        break
        except ClientError as ce:
            logger.debug(f"ClientError: {ce}")
        except Exception as e:
            print_error(f"Error reading {self.get_resource_type()}.")
            print_error(e)
        return self.active_resource

    def _delete(self, aws_client: AwsApiClient) -> bool:
        """Deletes the DbCluster

        Args:
            aws_client: The AwsApiClient for the current cluster
        """
        print_info(f"Deleting {self.get_resource_type()}: {self.get_resource_name()}")

        service_client = self.get_service_client(aws_client)
        self.active_resource = None

        # Step 1: Delete DbInstances
        if self.db_instances is not None:
            for db_instance in self.db_instances:
                db_instance._delete(aws_client)

        # Step 2: Delete DbCluster
        # create a dict of args which are not null, otherwise aws type validation fails
        not_null_args: Dict[str, Any] = {}
        if self.final_db_snapshot_identifier:
            not_null_args[
                "FinalDBSnapshotIdentifier"
            ] = self.final_db_snapshot_identifier

        try:
            db_cluster_identifier = self.get_db_cluster_identifier()
            delete_response = service_client.delete_db_cluster(
                DBClusterIdentifier=db_cluster_identifier,
                SkipFinalSnapshot=self.skip_final_snapshot,
                **not_null_args,
            )
            logger.debug(f"DbCluster: {delete_response}")
            print_info(
                f"{self.get_resource_type()}: {self.get_resource_name()} deleted"
            )
            return True
        except Exception as e:
            print_error(f"{self.get_resource_type()} could not be deleted.")
            print_error("Please try again or delete resources manually.")
            print_error(e)
        return False

    def post_delete(self, aws_client: AwsApiClient) -> bool:

        # Wait for DbCluster to be deleted
        if self.wait_for_deletion:
            try:
                print_info(f"Waiting for {self.get_resource_type()} to be deleted.")
                waiter = self.get_service_client(aws_client).get_waiter(
                    "db_cluster_deleted"
                )
                waiter.wait(
                    DBClusterIdentifier=self.get_db_cluster_identifier(),
                    WaiterConfig={
                        "Delay": self.waiter_delay,
                        "MaxAttempts": self.waiter_max_attempts,
                    },
                )
            except Exception as e:
                print_error("Waiter failed.")
                print_error(e)
        return True
