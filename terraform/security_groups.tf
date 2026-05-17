# terraform/security_groups.tf

resource "aws_security_group" "rds_sg" {
  name        = "medsched-rds-sg"
  description = "Allow inbound traffic from EKS to RDS PostgreSQL"
  vpc_id      = module.vpc.vpc_id

  # Inbound rule: Allow PostgreSQL traffic (Port 5432) from within the VPC
  ingress {
    description = "PostgreSQL traffic from VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }

  # Outbound rule: Allow the database to talk to the internet if needed (e.g., updates)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "medsched-rds-sg"
  }
}