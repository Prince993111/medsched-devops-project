# terraform/eks.tf

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "medsched-eks-cluster"
  cluster_version = "1.34"

  # Allows the cluster to be controlled via public endpoints (securely authenticated)
  # while keeping node-to-node communication strictly inside the private subnets
  cluster_endpoint_public_access = true

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.private_subnets

  # Managed Node Groups - These are the EC2 instances where your Docker containers will run
  eks_managed_node_groups = {
    medsched_nodes = {
      min_size     = 1
      max_size     = 3
      desired_size = 2

      instance_types = ["t3.small"] # Budget-friendly but powerful enough for K8s system pods
      capacity_type  = "SPOT"       # Uses AWS Spot instances to save up to 90% on cost while practicing

      tags = {
        Environment = "dev"
      }
    }
  }

  # Configures cluster access permissions for the creator (your PRINCE_devops user)
  enable_cluster_creator_admin_permissions = true

  tags = {
    Environment = "dev"
    Project     = "medsched"
  }
}