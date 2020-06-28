# ddd-django

A Sample Project of DDD with python django

Python 언어로 작성된 [DDD](https://martinfowler.com/tags/domain%20driven%20design.html) 샘플 프로젝트

## Project 구조

| 디렉토리 | 설명 |
| - | - |
| domain/article | Article 도메인 정의 예시 |
| article | Article 도메인을 사용하는 서비스 |

## Requirements

```bash
> pip3 install pip-tools
> pip3 install -r requirements.txt
```

### Installed packages

| Name | Description |
| - | - |
| django | Django Rest Framework |
| factory_boy | For Unit tests |
| flake8 | Lint |
| pylint-django | Lint |

### How to create an app

```python
> python3 manage.py startapp {{app_name}}
```
