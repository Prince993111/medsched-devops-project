# terraform/rds.tf

resource "aws_db_instance" "postgres" {
  identifier           = "medsched-db"
  allocated_storage    = 20                  # 20 GB is free-tier eligible
  max_allocated_storage = 100                # Allows auto-scaling storage if needed
  engine               = "postgres"
  engine_version       = "15"              # Production-stable PostgreSQL version
  instance_class       = "db.t3.micro"       # Free-tier friendly instance type
  
  # Database credentials (we'll make these dynamic/secure later)
  db_name              = "medsched"
  username             = "medadmin"
  password             = "SuperSecurePassword123!" # Change this later!
  
  # Network deployment placement
  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot    = true              # Allows fast destroying while practicing/testing

  tags = {
    Name = "medsched-database"
  }
}